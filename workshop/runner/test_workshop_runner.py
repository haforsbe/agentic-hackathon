import copy
import base64
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock, patch

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

    def test_documented_data_policy_accepts_existing_equivalent_or_broader_grant(self):
        for pattern in ("Microsoft.CognitiveServices/*", "MICROSOFT.COGNITIVESERVICES/*", "*"):
            for exclusions in ([], list(runner.FOUNDRY_USER_DATA_EXCLUSIONS)):
                with self.subTest(pattern=pattern, exclusions=exclusions):
                    self.assertTrue(runner.foundry_user_data_access([
                        {"dataActions": [pattern], "notDataActions": exclusions},
                    ]))

    def test_documented_data_policy_rejects_narrower_or_additionally_restricted_grants(self):
        for grants in (
            [],
            [{"actions": ["*"]}],
            [{"dataActions": ["Microsoft.CognitiveServices/accounts/AIServices/agents/*"]}],
            [{"dataActions": ["Microsoft.CognitiveServices/accounts/AIServices/agents/storage/read"]}],
            [{"dataActions": ["Microsoft.CognitiveServices/*"], "notDataActions": ["*/storage/write"]}],
            [{"dataActions": ["Microsoft.CognitiveServices/*"], "notDataActions": ["*"]}],
        ):
            with self.subTest(grants=grants):
                self.assertFalse(runner.foundry_user_data_access(grants))

    def test_independent_equivalent_grant_can_supply_access(self):
        restricted = {"dataActions": ["Microsoft.CognitiveServices/*"], "notDataActions": ["*/storage/*"]}
        self.assertTrue(runner.foundry_user_data_access([
            restricted, {"dataActions": ["Microsoft.CognitiveServices/*"]},
        ]))

    def verify_grants(self, grants, **extra):
        credential = Mock()
        credential.get_token.return_value.token = "synthetic-token"
        payload = io.StringIO(json.dumps({"value": grants, **extra}))
        with patch.object(runner, "urlopen", return_value=payload):
            return runner.verify_permissions(self.plan, credential)

    def test_permission_preflight_records_documented_data_policy(self):
        self.plan["authorization_policy"] = "foundry-user-data-access"
        verification = self.verify_grants([{
            "dataActions": ["Microsoft.CognitiveServices/*"],
            "notDataActions": list(runner.FOUNDRY_USER_DATA_EXCLUSIONS),
        }])
        self.assertEqual(verification["policy"], "foundry-user-data-access")
        self.assertTrue(verification["foundry_user_equivalent_data_grant_verified"])
        self.assertTrue(verification["required_permissions_verified"])
        self.client.conversations.create.assert_not_called()
        self.client.responses.create.assert_not_called()

    def test_documented_data_policy_still_checks_exact_required_operations(self):
        self.plan["authorization_policy"] = "foundry-user-data-access"
        self.plan["required_permissions"] = [{"kind": "actions", "operation": "Microsoft.Authorization/test/write"}]
        with self.assertRaisesRegex(ValueError, "Required operation permission"):
            self.verify_grants([{"dataActions": ["Microsoft.CognitiveServices/*"]}])

    def test_permission_preflight_rejects_missing_broad_grant_and_pagination(self):
        self.plan["authorization_policy"] = "foundry-user-data-access"
        with self.assertRaisesRegex(ValueError, "data grant not verified"):
            self.verify_grants([{"dataActions": [self.plan["required_permissions"][0]["operation"]]}])
        with self.assertRaisesRegex(ValueError, "pagination"):
            self.verify_grants([{"dataActions": ["*"]}], nextLink="https://synthetic.invalid/next")
        self.client.conversations.create.assert_not_called()
        self.client.responses.create.assert_not_called()

    def test_conversation_policy_is_checked_again_before_permission_request(self):
        self.plan["operation"] = "new-conversation"
        with patch.object(runner, "urlopen") as request:
            with self.assertRaisesRegex(ValueError, "Managed Conversations require"):
                runner.verify_permissions(self.plan, Mock())
        request.assert_not_called()

    def test_legacy_operation_specific_preflight_remains_supported(self):
        verification = self.verify_grants([{"dataActions": [self.plan["required_permissions"][0]["operation"]]}])
        self.assertEqual(verification, {"policy": "operation-specific", "required_permissions_verified": True})

    def test_normalization_accepts_only_equivalent_allowlist(self):
        a = {"tools": [{"allowed_tools": ["weather_forecast"]}]}
        b = {"tools": [{"allowed_tools": {"tool_names": ["weather_forecast"]}}]}
        self.assertEqual(runner.normalized(a), runner.normalized(b))
        b["tools"][0]["allowed_tools"]["other"] = True
        with self.assertRaises(ValueError):
            runner.normalized(b)


class CredentialTokenCacheTests(unittest.TestCase):
    scope = "https://management.azure.com/.default"

    def setUp(self):
        self.plan = plan()
        clock_patch = patch.object(runner, "time", return_value=1000)
        self.clock = clock_patch.start()
        self.addCleanup(clock_patch.stop)
        profile_patch = patch.dict(runner.os.environ, {"AZURE_CONFIG_DIR": self.plan["azure_config_dir"]})
        profile_patch.start()
        self.addCleanup(profile_patch.stop)
        self.inner = Mock()
        self.inner.get_token.return_value = self.token()
        identity = SimpleNamespace(AzureCliCredential=Mock(return_value=self.inner))
        with patch.dict("sys.modules", {"azure.identity": identity}):
            self.credential = runner.verified_credential(self.plan)
        self.addCleanup(self.credential.close)

    def token(self, expires_on=2000, **overrides):
        claims = {
            "upn": self.plan["account"], "tid": self.plan["tenant"],
            "aud": "https://management.azure.com/", "exp": 2000,
        }
        claims.update(overrides)
        payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
        return SimpleNamespace(token=f"header.{payload}.signature", expires_on=expires_on)

    def test_exact_arm_token_is_reused_and_permission_http_is_not_cached(self):
        grants = {"value": [{"dataActions": [self.plan["required_permissions"][0]["operation"]]}]}
        token = self.credential.get_token(self.scope)
        self.assertIs(self.credential.get_token(self.scope), token)
        with patch.object(runner, "urlopen", side_effect=lambda *a, **k: io.StringIO(json.dumps(grants))) as request:
            for _ in range(2):
                self.assertTrue(runner.verify_permissions(
                    self.plan, self.credential)["required_permissions_verified"])
        self.inner.get_token.assert_called_once_with(self.scope)
        self.assertEqual(request.call_count, 2)

    def test_both_expiry_fields_require_five_minutes_remaining(self):
        for options in ({"expires_on": 1300}, {"exp": 1300}, {"expires_on": None}, {"exp": None}):
            with self.subTest(options=options):
                self.credential.arm_token = None
                self.inner.get_token.reset_mock()
                self.inner.get_token.return_value = self.token(**options)
                self.credential.get_token(self.scope)
                self.credential.get_token(self.scope)
                self.assertEqual(self.inner.get_token.call_count, 2)

    def test_cached_token_is_refreshed_before_expiry(self):
        self.credential.get_token(self.scope)
        self.clock.return_value = 1700
        fresh = self.token(expires_on=3000, exp=3000)
        self.inner.get_token.return_value = fresh
        self.assertIs(self.credential.get_token(self.scope), fresh)
        self.assertEqual(self.inner.get_token.call_count, 2)

    def test_other_audiences_and_missing_audience_are_not_cached(self):
        for audience in (None, "https://ai.azure.com", self.scope):
            with self.subTest(audience=audience):
                self.inner.get_token.reset_mock()
                self.inner.get_token.return_value = self.token(aud=audience)
                self.credential.get_token(self.scope)
                self.credential.get_token(self.scope)
                self.assertEqual(self.inner.get_token.call_count, 2)

    def test_options_other_scopes_and_multiple_scopes_do_not_reuse_arm_token(self):
        calls = [
            ((self.scope,), {"tenant_id": self.plan["tenant"]}),
            ((self.scope,), {"claims": "synthetic-claims"}),
            ((self.scope,), {"enable_cae": False}),
            (("https://ai.azure.com/.default",), {}),
            ((self.scope, "https://ai.azure.com/.default"), {}),
        ]
        for scopes, options in calls:
            with self.subTest(scopes=scopes, options=options):
                self.credential.get_token(self.scope)
                self.inner.get_token.reset_mock()
                self.credential.get_token(*scopes, **options)
                self.credential.get_token(*scopes, **options)
                self.assertEqual(self.inner.get_token.call_count, 2)
                self.inner.get_token.assert_called_with(*scopes, **options)

    def test_cli_profile_or_process_change_invalidates_cached_token(self):
        self.credential.get_token(self.scope)
        with patch.dict(runner.os.environ, {"AZURE_CONFIG_DIR": "another-synthetic-profile"}):
            self.credential.get_token(self.scope)
        self.credential.get_token(self.scope)
        with patch.object(runner.os, "getpid", return_value=-1):
            self.credential.get_token(self.scope)
        self.assertEqual(self.inner.get_token.call_count, 4)

    def test_changed_confirmed_identity_does_not_reuse_old_token(self):
        for field in ("account", "tenant", "subscription"):
            with self.subTest(field=field):
                self.credential.arm_token = None
                self.credential.get_token(self.scope)
                old_value = self.plan[field]
                self.plan[field] = "different-synthetic-value"
                self.inner.get_token.reset_mock()
                if field == "subscription":
                    self.credential.get_token(self.scope)
                else:
                    with patch.object(runner, "check_cli", side_effect=ValueError("identity differs")):
                        with self.assertRaisesRegex(ValueError, "identity differs"):
                            self.credential.get_token(self.scope)
                self.inner.get_token.assert_called_once_with(self.scope)
                self.plan[field] = old_value

    def test_alias_identity_checks_are_repeated_on_cache_hit(self):
        self.inner.get_token.return_value = self.token(upn="alias@example.invalid", oid="synthetic-user-id")
        with patch.object(runner, "check_cli") as account_check, patch.object(
            runner, "cli", return_value="synthetic-user-id",
        ) as directory_check:
            self.credential.get_token(self.scope)
            self.credential.get_token(self.scope)
            self.assertEqual(account_check.call_count, 2)
            self.assertEqual(directory_check.call_count, 2)
            directory_check.return_value = "different-user-id"
            with self.assertRaisesRegex(ValueError, "identity differs"):
                self.credential.get_token(self.scope)
        self.assertIsNone(self.credential.arm_token)
        self.inner.get_token.assert_called_once_with(self.scope)

    def test_failed_identity_verification_does_not_cache_token(self):
        self.inner.get_token.return_value = self.token(tid="different-tenant")
        for _ in range(2):
            with self.assertRaisesRegex(ValueError, "identity differs"):
                self.credential.get_token(self.scope)
        self.assertIsNone(self.credential.arm_token)
        self.assertEqual(self.inner.get_token.call_count, 2)

    def test_close_clears_token_and_prevents_reuse(self):
        self.credential.get_token(self.scope)
        self.credential.close()
        self.assertIsNone(self.credential.arm_token)
        with self.assertRaisesRegex(ValueError, "closed"):
            self.credential.get_token(self.scope)

    def test_acquisition_failure_has_no_retry_or_cached_fallback(self):
        self.credential.get_token(self.scope)
        self.clock.return_value = 1700
        self.inner.get_token.reset_mock()
        self.inner.get_token.side_effect = RuntimeError("synthetic credential failure")
        with self.assertRaisesRegex(RuntimeError, "synthetic credential failure"):
            self.credential.get_token(self.scope)
        self.assertIsNone(self.credential.arm_token)
        self.inner.get_token.assert_called_once_with(self.scope)


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

    def test_unknown_authorization_policy_is_rejected(self):
        self.plan["authorization_policy"] = "skip-permissions"
        with self.assertRaisesRegex(ValueError, "Unsupported authorization policy"):
            self.load()

    def test_managed_conversation_requires_explicit_documented_data_policy(self):
        for operation in ("new-conversation", "run"):
            with self.subTest(operation=operation):
                self.plan["operation"] = operation
                self.plan["cases"][0]["conversation_id"] = "conv_synthetic"
                with self.assertRaisesRegex(ValueError, "Managed Conversations require"):
                    self.load()
                self.plan["authorization_policy"] = "foundry-user-data-access"
                self.assertEqual(self.load()[0]["authorization_policy"], "foundry-user-data-access")
                self.plan.pop("authorization_policy")

    def test_documented_data_policy_does_not_replace_required_permissions(self):
        self.plan["authorization_policy"] = "foundry-user-data-access"
        for permissions in ([], [{"kind": "dataActions", "operation": "Microsoft.CognitiveServices/*"}]):
            with self.subTest(permissions=permissions):
                self.plan["required_permissions"] = permissions
                with self.assertRaises(ValueError):
                    self.load()

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

    def test_missing_data_policy_grant_stops_before_constructing_project_client(self):
        self.plan.update(operation="new-conversation", authorization_policy="foundry-user-data-access")
        project_factory = Mock()
        credential = Mock()
        credential.get_token.return_value.token = "synthetic-token"
        payload = io.StringIO(json.dumps({
            "value": [{"dataActions": [self.plan["required_permissions"][0]["operation"]]}],
        }))
        with patch.dict("sys.modules", {"azure.ai.projects": SimpleNamespace(AIProjectClient=project_factory)}), \
                patch.object(runner, "readiness", return_value={"prompt_runner_ready": True}), \
                patch.object(runner, "check_cli"), \
                patch.object(runner, "cli", return_value={"id": self.plan["project_resource_id"]}), \
                patch.object(runner, "verified_credential", return_value=credential), \
                patch.object(runner, "urlopen", return_value=payload), \
                patch.dict(runner.os.environ):
            with self.assertRaisesRegex(RuntimeError, "Runner stopped"):
                runner.run(self.plan, CONFIG)
        project_factory.assert_not_called()
        credential.close.assert_called_once()
        evidence = json.loads((self.root / ".workshop" / "evidence" / "synthetic-test.json").read_text())
        self.assertEqual(evidence["state"], "stopped_do_not_retry_without_reconciliation")
        self.assertEqual(evidence["requests_started"], 0)
        self.assertIn("data grant not verified", evidence["error"]["reason"])

    def test_project_access_reads_only_first_connection_page_and_propagates_failure(self):
        for index, (items, fails) in enumerate((([], False), ([{"name": "synthetic"}], False), ([], True))):
            with self.subTest(items=items, fails=fails):
                self.plan.update(operation="inspect", run_id=f"synthetic-access-{index}")
                project_factory = MagicMock()
                project = project_factory.return_value.__enter__.return_value
                project.agents.get_version.return_value.definition.as_dict.return_value = CONFIG["definition"]
                client = project.get_openai_client.return_value.__enter__.return_value
                credential = Mock()

                def pages():
                    if fails:
                        raise TimeoutError("Synthetic project access failure")
                    yield iter(items)
                    self.fail("Project access must not fetch another connection page")

                listing = project.connections.list.return_value
                listing.by_page.return_value = pages()
                listing.__iter__.side_effect = AssertionError("Do not enumerate all connections")
                with patch.dict("sys.modules", {"azure.ai.projects": SimpleNamespace(AIProjectClient=project_factory)}), \
                        patch.object(runner, "readiness", return_value={"prompt_runner_ready": True}), \
                        patch.object(runner, "check_cli") as check_cli, \
                        patch.object(runner, "cli", return_value={"id": self.plan["project_resource_id"]}), \
                        patch.object(runner, "verified_credential", return_value=credential), \
                        patch.object(runner, "verify_permissions", return_value={"required_permissions_verified": True}) as permissions, \
                        patch.dict(runner.os.environ):
                    if fails:
                        with self.assertRaisesRegex(RuntimeError, "Runner stopped"):
                            runner.run(self.plan, CONFIG)
                    else:
                        _, record = runner.run(self.plan, CONFIG)
                        self.assertEqual(record["state"], "operation_completed_not_graded")
                        project.agents.get_version.assert_called_once_with(
                            agent_name=self.plan["agent_name"], agent_version=self.plan["agent_version"])
                        project.get_openai_client.assert_called_once_with(max_retries=0, timeout=60)
                check_cli.assert_called_once_with(self.plan)
                permissions.assert_called_once_with(self.plan, credential)
                project_factory.assert_called_once_with(
                    endpoint=self.plan["endpoint"], credential=credential, retry_total=0)
                listing.by_page.assert_called_once_with()
                client.responses.create.assert_not_called()
                credential.close.assert_called_once()
                if fails:
                    project.get_openai_client.assert_not_called()
                    project.agents.get_version.assert_not_called()
                    evidence = json.loads(
                        (self.root / ".workshop" / "evidence" / f"synthetic-access-{index}.json").read_text())
                    self.assertEqual(evidence["state"], "stopped_do_not_retry_without_reconciliation")
                    self.assertEqual(evidence["requests_started"], 0)
                    self.assertEqual(evidence["error"]["type"], "TimeoutError")


if __name__ == "__main__":
    unittest.main()
