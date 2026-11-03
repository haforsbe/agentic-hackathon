import copy
import base64
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import workshop_runner as runner


REFERENCE = {"type": "agent_reference", "name": "synthetic-weather", "version": "4"}
CONFIG = {
    "name": "synthetic-weather",
    "definition": {"kind": "prompt", "model": "chosen-model", "instructions": "Synthetic instructions", "tools": []},
}


def plan():
    return {
        "operation": "run", "run_id": "synthetic-test", "approval_reference": "synthetic-user-turn",
        "public_or_synthetic_data_only": True, "account": "student@example.invalid",
        "tenant": "synthetic-tenant", "subscription": "synthetic-subscription",
        "azure_config_dir": str(Path(tempfile.gettempdir()) / "synthetic-workshop-profile"),
        "endpoint": "https://synthetic.services.ai.azure.com/api/projects/synthetic",
        "project_resource_id": "/subscriptions/synthetic-subscription/resourceGroups/test/providers/Microsoft.CognitiveServices/accounts/synthetic/projects/synthetic",
        "required_permissions": [{"kind": "dataActions", "operation": "Microsoft.CognitiveServices/test/action"}],
        "agent_name": "synthetic-weather", "agent_version": "4", "configuration": "student/agent.json",
        "max_output_tokens": 200, "max_requests": 2,
        "cases": [{"id": "B01", "prompt": "Synthetic first prompt"}, {"id": "B02", "prompt": "Synthetic second prompt"}],
    }


def response(output=None, version="4", status="completed"):
    body = {
        "id": "resp_synthetic", "agent_reference": {**REFERENCE, "version": version},
        "output": output or [{"type": "message"}], "status": status, "usage": None,
    }
    return SimpleNamespace(
        id=body["id"], status=status, output_text="Synthetic answer",
        model_dump=lambda **kwargs: copy.deepcopy(body),
    )


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.plan = plan()
        self.record = {"state": "preflight", "requests_started": 0, "results": []}
        self.project = Mock()
        self.project.agents.get_version.return_value.definition.as_dict.return_value = CONFIG["definition"]
        self.client = Mock()
        self.client.responses.create.return_value = response()
        self.cli_patch = patch.object(runner, "check_cli")
        self.cli_patch.start()
        self.addCleanup(self.cli_patch.stop)

    def execute(self):
        runner.execute(self.project, self.client, self.plan, CONFIG, self.record, lambda: None)

    def test_batch_is_pinned_bounded_fresh_and_has_no_retries(self):
        self.execute()
        self.assertEqual(self.record["requests_started"], 2)
        for call in self.client.responses.create.call_args_list:
            kwargs = call.kwargs
            self.assertEqual(kwargs["extra_body"], {"agent_reference": REFERENCE})
            self.assertEqual(kwargs["max_output_tokens"], 200)
            self.assertFalse(kwargs["store"])
            self.assertNotIn("conversation", kwargs)
            self.assertNotIn("previous_response_id", kwargs)
        self.assertEqual(len(self.record["results"]), 2)
        self.assertIsNone(self.record["results"][0]["usage"])

    def test_pending_tool_stops_batch_without_approval(self):
        self.client.responses.create.return_value = response([{"type": "mcp_approval_request", "id": "mcpr_test"}])
        self.execute()
        self.assertEqual(self.client.responses.create.call_count, 1)
        self.assertEqual(self.record["state"], "awaiting_separate_tool_approval")

    def test_version_mismatch_is_not_a_pass_and_keeps_raw_response(self):
        self.client.responses.create.return_value = response(version="3")
        with self.assertRaisesRegex(ValueError, "linkage"):
            self.execute()
        self.assertEqual(self.record["raw_response"]["agent_reference"]["version"], "3")
        self.assertEqual(self.record["results"], [])
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_incomplete_response_stops_without_another_request(self):
        self.client.responses.create.return_value = response(status="incomplete")
        with self.assertRaisesRegex(ValueError, "incomplete"):
            self.execute()
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_exception_keeps_started_marker_no_automatic_repeat(self):
        self.client.responses.create.side_effect = TimeoutError()
        with self.assertRaises(TimeoutError):
            self.execute()
        self.assertEqual(self.record["state"], "request_started_do_not_repeat")
        self.assertEqual(self.record["requests_started"], 1)
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_existing_conversation_is_explicit_and_stored(self):
        self.plan["cases"] = [{"id": "D01-followup", "prompt": "Synthetic follow-up", "conversation_id": "conv_synthetic"}]
        self.execute()
        kwargs = self.client.responses.create.call_args.kwargs
        self.assertEqual(kwargs["conversation"], "conv_synthetic")
        self.assertTrue(kwargs["store"])

    def test_explicit_response_storage_does_not_add_conversation_history(self):
        self.plan["cases"] = [{"id": "C01", "prompt": "Synthetic forecast", "store": True}]
        self.execute()
        kwargs = self.client.responses.create.call_args.kwargs
        self.assertTrue(kwargs["store"])
        self.assertNotIn("conversation", kwargs)
        self.assertNotIn("previous_response_id", kwargs)

    def test_config_drift_stops_before_model_request(self):
        self.project.agents.get_version.return_value.definition.as_dict.return_value = {"kind": "prompt"}
        with self.assertRaisesRegex(ValueError, "configuration"):
            self.execute()
        self.client.responses.create.assert_not_called()

    def test_readonly_retrieval_never_creates_a_response(self):
        self.plan.update(operation="retrieve", response_id="resp_synthetic")
        self.client.responses.retrieve.return_value = response()
        self.execute()
        self.client.responses.create.assert_not_called()
        self.assertEqual(self.record["requests_started"], 0)

    def test_creation_readback_does_not_invoke_a_model(self):
        self.plan["operation"] = "create-version"
        self.project.agents.create_version.return_value.version = "5"
        definition = Mock()
        definition.as_dict.return_value = CONFIG["definition"]
        models = SimpleNamespace(MCPTool=Mock(), PromptAgentDefinition=Mock(return_value=definition))
        with patch.dict("sys.modules", {"azure.ai.projects.models": models}):
            self.execute()
        self.project.agents.create_version.assert_called_once()
        self.project.agents.get_version.assert_called_once_with(agent_name="synthetic-weather", agent_version="5")
        self.client.responses.create.assert_not_called()
        self.assertTrue(self.record["definition_readback_matches"])
        self.assertEqual(self.record["created_version"], "5")

    def test_new_conversation_has_its_own_write_marker_and_no_model_call(self):
        self.plan["operation"] = "new-conversation"
        self.client.conversations.create.return_value.id = "conv_created"
        states = []
        runner.execute(self.project, self.client, self.plan, CONFIG, self.record,
                       lambda: states.append(self.record["state"]))
        self.assertIn("conversation_creation_started_do_not_repeat", states)
        self.assertEqual(self.record["conversation_id"], "conv_created")
        self.client.responses.create.assert_not_called()

    def test_cli_mismatch_stops_without_switching_identity(self):
        with patch.object(runner, "cli", return_value={
            "user": {"name": "another@example.invalid"}, "tenantId": self.plan["tenant"], "id": self.plan["subscription"],
        }):
            # setUp replaces check_cli to isolate other tests.
            with self.assertRaisesRegex(ValueError, "differs"):
                self.real_check_cli(self.plan)

    real_check_cli = staticmethod(runner.check_cli)

    def test_actual_sdk_credential_must_match_participant(self):
        def token(account, tenant):
            payload = base64.urlsafe_b64encode(json.dumps({"upn": account, "tid": tenant}).encode()).decode().rstrip("=")
            return SimpleNamespace(token=f"header.{payload}.signature")

        inner = Mock()
        inner.get_token.return_value = token(self.plan["account"], self.plan["tenant"])
        identity = SimpleNamespace(AzureCliCredential=Mock(return_value=inner))
        with patch.dict("sys.modules", {"azure.identity": identity}):
            credential = runner.verified_credential(self.plan)
        self.assertIsNotNone(credential.get_token("https://ai.azure.com/.default"))
        inner.get_token.return_value = token("another@example.invalid", self.plan["tenant"])
        with (
            patch.object(runner, "cli", return_value="synthetic-user-id"),
            self.assertRaisesRegex(ValueError, "identity differs"),
        ):
            credential.get_token("https://ai.azure.com/.default")
        credential.close()
        inner.close.assert_called_once()

    def test_tool_continuation_checks_exact_arguments_and_allows_denial(self):
        self.plan.update(
            operation="continue", response_id="resp_synthetic", approval_request_id="mcpr_synthetic",
            tool_name="weather_forecast", server_label="weather_intelligence", arguments={"lat": 40, "lon": -74},
            approve=False,
        )
        self.plan.pop("cases")
        self.client.responses.retrieve.return_value = response([{
            "type": "mcp_approval_request", "id": "mcpr_synthetic", "name": "weather_forecast",
            "server_label": "weather_intelligence", "arguments": '{"lat":40,"lon":-74}',
        }])
        self.execute()
        kwargs = self.client.responses.create.call_args.kwargs
        self.assertFalse(kwargs["input"][0]["approve"])
        self.assertEqual(kwargs["previous_response_id"], "resp_synthetic")
        self.plan["arguments"] = {"lat": 0, "lon": 0}
        self.client.responses.create.reset_mock()
        with self.assertRaisesRegex(ValueError, "scope differs"):
            self.execute()
        self.client.responses.create.assert_not_called()

    def test_permission_wildcards_exclusions_and_independent_grants(self):
        grants = [{"dataActions": ["Microsoft.CognitiveServices/*"], "notDataActions": ["*/test/*"]}]
        permission = self.plan["required_permissions"][0]
        self.assertFalse(runner.permitted(grants, permission))
        grants.append({"dataActions": [permission["operation"]]})
        self.assertTrue(runner.permitted(grants, permission))
        self.assertFalse(runner.permitted(grants, {"kind": "actions", "operation": permission["operation"]}))

    def test_normalization_accepts_only_equivalent_allowlist(self):
        a = {"tools": [{"allowed_tools": ["weather_forecast"]}]}
        b = {"tools": [{"allowed_tools": {"tool_names": ["weather_forecast"]}}]}
        self.assertEqual(runner.normalized(a), runner.normalized(b))
        b["tools"][0]["allowed_tools"]["other"] = True
        with self.assertRaises(ValueError):
            runner.normalized(b)


class CredentialAliasTests(unittest.TestCase):
    def setUp(self):
        self.plan = plan()
        self.inner = Mock()
        self.identity = SimpleNamespace(AzureCliCredential=Mock(return_value=self.inner))
        with patch.dict("sys.modules", {"azure.identity": self.identity}):
            self.credential = runner.verified_credential(self.plan)
        self.addCleanup(self.credential.close)
        self.account = {
            "user": {"name": self.plan["account"]},
            "tenantId": self.plan["tenant"], "id": self.plan["subscription"],
        }
        self.user_id = "synthetic-user-id"
        self.cli_patch = patch.object(runner, "cli", side_effect=self.cli)
        self.cli_mock = self.cli_patch.start()
        self.addCleanup(self.cli_patch.stop)

    def cli(self, *args):
        if args == ("account", "show"):
            return self.account
        self.assertEqual(args, ("ad", "signed-in-user", "show", "--query", "id"))
        return self.user_id

    def token(self, **overrides):
        claims = {
            "upn": "alias@example.invalid", "tid": self.plan["tenant"],
            "oid": "synthetic-user-id",
        }
        claims.update(overrides)
        payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
        token = SimpleNamespace(token=f"header.{payload}.signature")
        self.inner.get_token.return_value = token
        return token

    def test_alias_matches_directory_identity_across_scopes(self):
        for scope in ("https://management.azure.com/.default", "https://ai.azure.com/.default"):
            with self.subTest(scope=scope):
                token = self.token()
                self.assertIs(self.credential.get_token(scope), token)
        self.assertEqual(self.cli_mock.call_count, 4)
        self.identity.AzureCliCredential.assert_called_once_with(
            tenant_id=self.plan["tenant"], process_timeout=60)

    def test_exact_name_claims_need_no_directory_lookup(self):
        for claim in ("upn", "preferred_username", "unique_name"):
            with self.subTest(claim=claim):
                token = self.token(oid=None, **{claim: self.plan["account"].upper()})
                self.assertIs(self.credential.get_token("https://ai.azure.com/.default"), token)
        self.cli_mock.assert_not_called()

    def test_alias_with_different_or_missing_token_object_id_fails(self):
        for oid in ("different-user-id", None, "", 42):
            with self.subTest(oid=oid):
                self.token(oid=oid)
                with self.assertRaisesRegex(ValueError, "identity differs"):
                    self.credential.get_token("https://ai.azure.com/.default")
        self.token()
        payload = base64.urlsafe_b64encode(json.dumps({
            "upn": "alias@example.invalid", "tid": self.plan["tenant"],
        }).encode()).decode().rstrip("=")
        self.inner.get_token.return_value = SimpleNamespace(token=f"header.{payload}.signature")
        with self.assertRaisesRegex(ValueError, "identity differs"):
            self.credential.get_token("https://ai.azure.com/.default")

    def test_different_tenant_fails_before_directory_lookup(self):
        self.token(tid="different-tenant")
        with self.assertRaisesRegex(ValueError, "identity differs"):
            self.credential.get_token("https://ai.azure.com/.default")
        self.cli_mock.assert_not_called()

    def test_invalid_directory_lookup_fails_closed(self):
        for user_id in (None, "", "   ", {}, [], 42):
            with self.subTest(user_id=user_id):
                self.user_id = user_id
                self.token()
                with self.assertRaisesRegex(ValueError, "directory identity could not be verified"):
                    self.credential.get_token("https://ai.azure.com/.default")

    def test_failed_directory_lookup_fails_closed(self):
        self.token()
        self.cli_mock.side_effect = [self.account, ValueError("Azure CLI check failed")]
        with self.assertRaisesRegex(ValueError, "Azure CLI check failed"):
            self.credential.get_token("https://ai.azure.com/.default")

    def test_alias_rechecks_cli_scope_before_lookup(self):
        for field in ("account", "tenant", "subscription"):
            with self.subTest(field=field):
                self.account = {
                    "user": {"name": self.plan["account"]},
                    "tenantId": self.plan["tenant"], "id": self.plan["subscription"],
                }
                if field == "account":
                    self.account["user"]["name"] = "different@example.invalid"
                else:
                    self.account[{"tenant": "tenantId", "subscription": "id"}[field]] = "different"
                self.cli_mock.reset_mock()
                self.token()
                with self.assertRaisesRegex(ValueError, "differs; no identity switch"):
                    self.credential.get_token("https://ai.azure.com/.default")
                self.cli_mock.assert_called_once_with("account", "show")

    def test_directory_identity_is_not_cached_between_alias_requests(self):
        self.token()
        self.credential.get_token("https://management.azure.com/.default")
        self.user_id = "different-user-id"
        with self.assertRaisesRegex(ValueError, "identity differs"):
            self.credential.get_token("https://ai.azure.com/.default")
        self.assertEqual(self.cli_mock.call_count, 4)


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".workshop").mkdir()
        (self.root / "student").mkdir()
        (self.root / "student" / "agent.json").write_text(json.dumps(CONFIG), encoding="utf-8")
        self.plan = plan()
        self.root_patch = patch.object(runner, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def load(self):
        (self.root / ".workshop" / "plan.json").write_text(json.dumps(self.plan), encoding="utf-8")
        return runner.load_plan(".workshop/plan.json")

    def test_valid_plan(self):
        self.assertEqual(self.load()[0]["max_requests"], 2)

    def test_approval_scope_and_budget_required(self):
        for key, value in (("approval_reference", ""), ("max_requests", 1),
                           ("public_or_synthetic_data_only", False), ("max_output_tokens", True)):
            with self.subTest(key=key):
                original = self.plan[key]
                self.plan[key] = value
                with self.assertRaises(ValueError):
                    self.load()
                self.plan[key] = original

    def test_endpoint_and_configuration_cannot_escape_scope(self):
        for endpoint in ("http://synthetic.services.ai.azure.com/api/projects/synthetic",
                         "https://synthetic.services.ai.azure.com.attacker.invalid/api/projects/synthetic",
                         "https://user:password@synthetic.services.ai.azure.com/api/projects/synthetic"):
            self.plan["endpoint"] = endpoint
            with self.assertRaises(ValueError):
                self.load()
        with self.assertRaises(ValueError):
            runner.local_path("../outside.json", "student")

    def test_tool_config_needs_storage_and_cannot_bypass_approval(self):
        config = copy.deepcopy(CONFIG)
        config["definition"]["tools"] = [{
            "type": "mcp", "server_label": "weather_intelligence",
            "server_url": "https://weather.datakoot.com/mcp",
            "allowed_tools": ["weather_forecast"], "require_approval": "always",
        }]
        (self.root / "student" / "agent.json").write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "response storage"):
            self.load()
        for case in self.plan["cases"]:
            case["store"] = True
        self.load()
        config["definition"]["tools"][0]["require_approval"] = "never"
        (self.root / "student" / "agent.json").write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "approval always"):
            self.load()

    def test_existing_attempt_refused_before_any_cloud_call(self):
        folder = self.root / ".workshop" / "evidence"
        folder.mkdir()
        existing = folder / (self.plan["run_id"] + ".json")
        existing.write_text('{"state":"request_started_do_not_repeat"}', encoding="utf-8")
        # run() imports the optional SDK; patch it without requiring packages for offline tests.
        with patch.dict("sys.modules", {"azure.ai.projects": SimpleNamespace(AIProjectClient=Mock())}):
            with patch.object(runner, "readiness", return_value={"prompt_runner_ready": True}):
                with self.assertRaises(FileExistsError):
                    runner.run(self.plan, CONFIG)
        self.assertIn("request_started", existing.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
