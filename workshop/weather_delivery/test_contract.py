import copy
import hashlib
import unittest

from workshop.weather_delivery.contract import (
    ContractError,
    canonical_sha256,
    validate_capture_files,
    validate_capture_package,
    validation_cases_sha256,
    validate_manifest,
    validate_manifest_files,
    validate_release_evidence,
    validate_validation_evidence,
    write_ci_record,
)
from workshop.weather_delivery.progress import (
    advance_weather_delivery,
    choose_weather_delivery,
    route_after_weather_release,
    skip_blocked_weather_delivery,
)


def sha(char):
    return char * 64


def manifest():
    return {
        "schema_version": 1,
        "lab": {
            "project_count": 1,
            "classification": "training-compromise",
            "production_isolation": False,
        },
        "project_ref": "workshop-project",
        "released_agent": {
            "name": "weather-release",
            "version": "7",
            "stable_endpoint": "https://agents.example.invalid/weather",
            "endpoint_source": "service-read-back",
            "configuration_sha256": sha("0"),
        },
        "validation_agent": {
            "name": "weather-validation",
            "memory_scope_ref": "validation-memory",
        },
        "configuration_source_path": "student/weather-delivery/agent-definition.json",
        "configuration_sha256": sha("9"),
        "model_policy": {
            "deployment_ref": "participant-selected-model",
            "model": "participant-selected-model",
            "version": "participant-selected-version",
            "change_policy": "keep-existing",
        },
        "instructions": {
            "source_path": "student/weather-delivery/instructions.md",
            "sha256": sha("a"),
        },
        "toolbox": {
            "name": "weather-toolbox",
            "version": "3",
            "mcp_url": (
                "https://project.example.invalid/api/projects/lab/toolboxes/"
                "weather-toolbox/versions/3/mcp?api-version=v1"
            ),
            "endpoint_source": "service-read-back",
            "upstream_connection_ref": "weather-upstream-connection",
            "upstream_target": "https://weather.datakoot.com/mcp",
            "upstream_auth": "none",
            "toolbox_auth_connection_ref": "weather-toolbox-auth",
            "toolbox_auth_type": "verified-auth-type",
            "toolbox_auth_evidence_ref": "connection-readback-1",
            "tool_map": {
                "weather_forecast": "weather_tools___weather_forecast",
                "current_weather": "weather_tools___current_weather",
            },
            "require_approval": "always",
            "unverified_bindings": [],
        },
        "skill": {
            "revision": "weather-skill-revision",
            "delivery": "reviewed repository file",
            "sha256": sha("b"),
        },
        "memory": {
            "configuration_sha256": sha("c"),
            "released_scope_ref": "release-memory",
            "validation_scope_ref": "validation-memory",
            "contents_included": False,
        },
        "unverified_bindings": [],
    }


def capture_manifest():
    return {
        "schema_version": 1,
        "source_agent_name": "weather-dev",
        "source_agent_version": "7",
        "production_agent_name": "weather-prod",
        "production_stable_endpoint": (
            "https://project.example.invalid/api/projects/lab/agents/weather-prod/"
            "endpoint/protocols/openai/responses"
        ),
        "definition_sha256": sha("d"),
    }


def captured_definition():
    return {
        "schema_version": 1,
        "definition": {
            "kind": "prompt",
            "model": "participant-model",
            "instructions": "Weather instructions.",
            "tools": [],
        },
    }


class CapturePackageTests(unittest.TestCase):
    def test_capture_package_requires_distinct_agents_and_expected_prod_target(self):
        config = capture_manifest()
        definition = captured_definition()
        validate_capture_package(config, definition, expected_production_agent="weather-prod")
        with self.assertRaisesRegex(ContractError, "different configured Prod agent"):
            validate_capture_package(config, definition, expected_production_agent="other-prod")
        config["production_agent_name"] = config["source_agent_name"]
        with self.assertRaisesRegex(ContractError, "must be separate"):
            validate_capture_package(config, definition)

    def test_capture_package_rejects_credentials_and_changed_hash(self):
        config = capture_manifest()
        definition = captured_definition()
        definition["definition"]["api_key"] = "not-a-real-key"
        with self.assertRaisesRegex(ContractError, "credential-like field"):
            validate_capture_package(config, definition)

    def test_capture_files_verify_definition_hash(self):
        import json
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "manifest.json"
            definition_path = Path(directory) / "agent-definition.json"
            definition = captured_definition()
            payload = json.dumps(definition, sort_keys=True).encode()
            config = capture_manifest()
            config["definition_sha256"] = hashlib.sha256(payload).hexdigest()
            manifest_path.write_text(json.dumps(config), encoding="utf-8")
            definition_path.write_bytes(payload)
            validate_capture_files(manifest_path, definition_path)
            definition_path.write_text(json.dumps(captured_definition()), encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "hash differs"):
                validate_capture_files(manifest_path, definition_path)


def ci_run(config):
    return {
        "id": "1234",
        "attempt": 2,
        "repository": "example/workshop",
        "head_repository": "example/workshop",
        "head_sha": "1" * 40,
        "head_branch": "FY27",
        "workflow_path": ".github/workflows/weather-delivery-check.yml",
        "event": "push",
        "status": "completed",
        "conclusion": "success",
        "latest_attempt": 2,
        "artifact": {
            "name": "weather-delivery-1234-2",
            "run_id": "1234",
            "expired": False,
        },
        "record": {
            "schema_version": 1,
            "status": "manifest-contract-passed",
            "eligible_for_release": False,
            "source_commit": "1" * 40,
            "manifest_sha256": canonical_sha256(config),
            "cases_sha256": validation_cases_sha256(),
        },
    }


def validation_evidence(config):
    return {
        "schema_version": 1,
        "status": "passed",
        "source_commit": "1" * 40,
        "manifest_sha256": canonical_sha256(config),
        "cases_sha256": validation_cases_sha256(),
        "ci_run": ci_run(config),
        "runtime": {
            "project_ref": "workshop-project",
            "ci_identity_ref": "github-oidc-identity",
            "runtime_identity_ref": "participant-entra-identity",
            "validation_agent_name": "weather-validation",
            "validation_agent_version": "12",
            "validation_config_sha256": config["configuration_sha256"],
            "validation_memory_scope_ref": "validation-memory",
            "released_agent_name": "weather-release",
            "released_agent_version": "7",
            "released_config_sha256": config["released_agent"]["configuration_sha256"],
            "released_memory_scope_ref": "release-memory",
            "toolbox_auth_type": config["toolbox"]["toolbox_auth_type"],
            "toolbox_auth_evidence_ref": config["toolbox"]["toolbox_auth_evidence_ref"],
            "upstream_target": config["toolbox"]["upstream_target"],
            "upstream_tools": sorted(config["toolbox"]["tool_map"]),
            "instructions_sha256": config["instructions"]["sha256"],
            "model_deployment_ref": config["model_policy"]["deployment_ref"],
            "model_name": config["model_policy"]["model"],
            "model_version": config["model_policy"]["version"],
            "skill_revision": config["skill"]["revision"],
            "skill_delivery": config["skill"]["delivery"],
            "skill_sha256": config["skill"]["sha256"],
            "memory_configuration_sha256": config["memory"]["configuration_sha256"],
            "toolbox_name": "weather-toolbox",
            "toolbox_version": "3",
            "toolbox_mcp_url": config["toolbox"]["mcp_url"],
            "upstream_connection_ref": "weather-upstream-connection",
            "toolbox_auth_connection_ref": "weather-toolbox-auth",
            "effective_tool_names": sorted(config["toolbox"]["tool_map"].values()),
            "unverified_bindings": [],
        },
        "checks": {
            check_id: {"status": "passed", "evidence_id": f"foundry-{check_id.lower()}"}
            for check_id in ("WD02", "WD03", "WD04")
        },
        "tool_calls": [
            {
                "decision": "approved",
                "tool_name": "weather_tools___weather_forecast",
                "arguments_sha256": sha("e"),
                "response_id": "response-approved",
                "conversation_id": "conversation-approved",
                "approval_request_id": "approval-approved",
                "trace_id": "trace-approved",
                "continuation_conversation_id": "conversation-approved",
                "execution_id": "execution-approved",
                "toolbox_version": "3",
            },
            {
                "decision": "denied",
                "tool_name": "weather_tools___weather_forecast",
                "arguments_sha256": sha("f"),
                "response_id": "response-denied",
                "conversation_id": "conversation-denied",
                "approval_request_id": "approval-denied",
                "trace_id": "trace-denied",
                "continuation_conversation_id": "conversation-denied",
                "execution_id": None,
                "toolbox_version": "3",
            },
        ],
    }


def release_evidence(validation):
    return {
        "schema_version": 1,
        "status": "passed",
        "source_commit": validation["source_commit"],
        "manifest_sha256": validation["manifest_sha256"],
        "ci_run_id": validation["ci_run"]["id"],
        "validation_candidate_version": validation["runtime"]["validation_agent_version"],
        "release_config_sha256": validation["runtime"]["validation_config_sha256"],
        "released_agent_name": "weather-release",
        "released_agent_version": "8",
        "stable_endpoint": "https://agents.example.invalid/weather",
        "endpoint_source": "service-read-back",
        "consumer_test": {
            "status": "passed",
            "response_id": "consumer-response",
            "conversation_id": "consumer-conversation",
            "trace_id": "consumer-trace",
            "evidence_id": "consumer-evidence",
            "agent_version": "8",
        },
    }


class ManifestTests(unittest.TestCase):
    def test_synthetic_manifest_passes(self):
        config = manifest()
        self.assertEqual(validate_manifest(config), config)

    def test_manifest_file_hashes_must_match_reviewed_files(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "student/weather-delivery").mkdir(parents=True)
            definition = b'{"agent":"weather"}\n'
            instructions = b"Weather instructions\n"
            definition_path = root / "student/weather-delivery/agent-definition.json"
            instructions_path = root / "student/weather-delivery/instructions.md"
            definition_path.write_bytes(definition)
            instructions_path.write_bytes(instructions)
            config = manifest()
            config["configuration_sha256"] = hashlib.sha256(definition).hexdigest()
            config["instructions"]["sha256"] = hashlib.sha256(instructions).hexdigest()

            self.assertEqual(validate_manifest_files(config, root), config)
            instructions_path.write_text("changed after review\n", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "instructions file hash"):
                validate_manifest_files(config, root)

    def test_manifest_paths_cannot_escape_student_folder(self):
        for field in ("configuration_source_path", "instructions"):
            with self.subTest(field=field):
                config = manifest()
                if field == "instructions":
                    config["instructions"]["source_path"] = "student/../private.md"
                else:
                    config[field] = "student/../private.json"
                with self.assertRaisesRegex(ContractError, "safe path"):
                    validate_manifest(config)

    def test_one_project_is_labeled_as_a_compromise(self):
        config = manifest()
        config["lab"]["production_isolation"] = True
        with self.assertRaisesRegex(ContractError, "training compromise"):
            validate_manifest(config)

    def test_release_and_validation_agent_must_be_separate(self):
        config = manifest()
        config["validation_agent"]["name"] = config["released_agent"]["name"]
        with self.assertRaisesRegex(ContractError, "separate agent"):
            validate_manifest(config)

    def test_memory_scope_must_be_explicitly_separate(self):
        config = manifest()
        config["memory"]["validation_scope_ref"] = config["memory"]["released_scope_ref"]
        config["validation_agent"]["memory_scope_ref"] = config["memory"]["released_scope_ref"]
        with self.assertRaisesRegex(ContractError, "memory scopes"):
            validate_manifest(config)

    def test_candidate_config_hash_must_match_reviewed_configuration(self):
        config = manifest()
        config["configuration_sha256"] = sha("1")
        evidence = validation_evidence(config)
        evidence["runtime"]["validation_config_sha256"] = sha("2")
        with self.assertRaisesRegex(ContractError, "configuration"):
            validate_validation_evidence(
                config,
                evidence,
                repository="example/workshop",
                default_branch="FY27",
                current_commit="1" * 40,
                latest_sha="1" * 40,
                latest_attempt=2,
            )

    def test_toolbox_auth_and_upstream_connections_must_be_distinct(self):
        config = manifest()
        config["toolbox"]["toolbox_auth_connection_ref"] = (
            config["toolbox"]["upstream_connection_ref"]
        )
        with self.assertRaisesRegex(ContractError, "must be distinct"):
            validate_manifest(config)

    def test_unverified_bindings_fail_closed(self):
        config = manifest()
        config["toolbox"]["unverified_bindings"] = ["unknown-connection"]
        with self.assertRaisesRegex(ContractError, "unverified bindings"):
            validate_manifest(config)

    def test_unknown_fields_fail_instead_of_being_dropped(self):
        config = manifest()
        config["toolbox"]["authorization_header"] = "Bearer secret"
        with self.assertRaisesRegex(ContractError, "exactly"):
            validate_manifest(config)

    def test_toolbox_endpoint_must_be_pinned_and_service_returned(self):
        config = manifest()
        config["toolbox"]["mcp_url"] = (
            "https://project.example.invalid/api/projects/lab/toolboxes/"
            "weather-toolbox/mcp?api-version=v1"
        )
        with self.assertRaisesRegex(ContractError, "version-specific"):
            validate_manifest(config)

    def test_stable_endpoint_cannot_be_a_toolbox_or_project_url(self):
        config = manifest()
        config["released_agent"]["stable_endpoint"] = config["toolbox"]["mcp_url"]
        with self.assertRaisesRegex(ContractError, "stable agent consumer endpoint"):
            validate_manifest(config)

    def test_private_memory_contents_are_rejected(self):
        config = manifest()
        config["memory"]["contents_included"] = True
        with self.assertRaisesRegex(ContractError, "contents"):
            validate_manifest(config)


class ValidationEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.manifest = manifest()
        self.evidence = validation_evidence(self.manifest)
        self.context = {
            "repository": "example/workshop",
            "default_branch": "FY27",
            "current_commit": "1" * 40,
            "latest_sha": "1" * 40,
            "latest_attempt": 2,
        }

    def check(self, evidence=None):
        return validate_validation_evidence(
            self.manifest, evidence or self.evidence, **self.context,
        )

    def test_valid_validation_evidence_passes(self):
        self.assertTrue(self.check())

    def test_failure_does_not_mutate_or_discard_partial_evidence(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["status"] = "failed"
        before = copy.deepcopy(evidence)
        with self.assertRaisesRegex(ContractError, "preserve its evidence"):
            self.check(evidence)
        self.assertEqual(evidence, before)

    def test_manifest_hash_must_match_reviewed_configuration(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["manifest_sha256"] = sha("0")
        with self.assertRaisesRegex(ContractError, "does not match"):
            self.check(evidence)

    def test_wrong_artifact_is_rejected(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["ci_run"]["artifact"]["name"] = "weather-delivery-1234-1"
        with self.assertRaisesRegex(ContractError, "default-branch commit"):
            self.check(evidence)

    def test_case_hash_must_match_the_reviewed_contract(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["cases_sha256"] = sha("0")
        with self.assertRaisesRegex(ContractError, "case definition"):
            self.check(evidence)

    def test_validation_must_use_current_commit_and_latest_default_branch_run(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["ci_run"]["head_sha"] = "2" * 40
        with self.assertRaisesRegex(ContractError, "default-branch commit"):
            self.check(evidence)

    def test_stale_ci_attempt_is_rejected(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["ci_run"]["latest_attempt"] = 1
        with self.assertRaisesRegex(ContractError, "default-branch commit"):
            self.check(evidence)

    def test_other_repository_or_workflow_is_rejected(self):
        for field, value in (
            ("repository", "attacker/workshop"),
            ("workflow_path", ".github/workflows/other.yml"),
        ):
            with self.subTest(field=field):
                evidence = copy.deepcopy(self.evidence)
                evidence["ci_run"][field] = value
                with self.assertRaises(ContractError):
                    self.check(evidence)

    def test_runtime_identity_must_not_be_confused_with_ci_identity(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["runtime"]["runtime_identity_ref"] = evidence["runtime"]["ci_identity_ref"]
        with self.assertRaisesRegex(ContractError, "identity"):
            self.check(evidence)

    def test_conversation_separation_does_not_replace_memory_scope_check(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["runtime"]["released_memory_scope_ref"] = "validation-memory"
        with self.assertRaisesRegex(ContractError, "candidate boundary"):
            self.check(evidence)

    def test_validation_must_not_change_released_agent_configuration(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["runtime"]["released_config_sha256"] = sha("8")
        with self.assertRaisesRegex(ContractError, "pinned dependencies"):
            self.check(evidence)

    def test_tool_calls_need_both_real_approval_outcomes(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["tool_calls"][1]["decision"] = "approved"
        evidence["tool_calls"][1]["execution_id"] = "execution-2"
        with self.assertRaisesRegex(ContractError, "approved call and a denied call"):
            self.check(evidence)

    def test_denial_must_not_have_an_execution_id(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["tool_calls"][1]["execution_id"] = "execution-denied"
        with self.assertRaisesRegex(ContractError, "must not have an execution ID"):
            self.check(evidence)

    def test_approval_continuation_must_use_the_same_conversation(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["tool_calls"][0]["continuation_conversation_id"] = "different-conversation"
        with self.assertRaisesRegex(ContractError, "same managed Conversation"):
            self.check(evidence)

    def test_unknown_tool_is_not_silently_removed(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["tool_calls"][0]["tool_name"] = "weather_tools___delete_everything"
        with self.assertRaisesRegex(ContractError, "outside the reviewed"):
            self.check(evidence)

    def test_release_requires_matching_validation_and_consumer_path(self):
        release = release_evidence(self.evidence)
        self.assertTrue(validate_release_evidence(
            self.manifest, self.evidence, release, **self.context,
        ))
        release["stable_endpoint"] = "https://project.example.invalid/api/projects/lab"
        with self.assertRaises(ContractError):
            validate_release_evidence(
                self.manifest, self.evidence, release, **self.context,
            )

    def test_release_cannot_reference_a_different_validation_attempt(self):
        release = release_evidence(self.evidence)
        release["ci_run_id"] = "9999"
        with self.assertRaises(ContractError):
            validate_release_evidence(
                self.manifest, self.evidence, release, **self.context,
            )


class OptionalRouteTests(unittest.TestCase):
    def test_v9_template_keeps_channel_gates_separate_from_optional_lab(self):
        import json
        from pathlib import Path

        progress = json.loads(
            (Path(__file__).resolve().parents[1] / "templates" / "progress.json").read_text()
        )
        self.assertEqual(progress["curriculum_version"], "two-specialists-workflow-v9")
        self.assertEqual(set(progress["channel_publications"]), {"weather", "workflow"})
        progress["current_checkpoint"] = "07"
        weather = next(item for item in progress["checkpoints"] if item["id"] == "07")
        weather["status"] = "blocked"
        self.assertEqual(route_after_weather_release(progress), "07")
        with self.assertRaises(ValueError):
            choose_weather_delivery(progress, "skip")

        weather["status"] = "passed"
        progress["channel_publications"]["weather"].update(
            status="passed", channel_test_evidence=["synthetic-CH01"]
        )
        original = copy.deepcopy(progress)
        for choice in ("start", "skip"):
            with self.subTest(choice=choice):
                updated = choose_weather_delivery(progress, choice)
                self.assertEqual(updated["channel_publications"], original["channel_publications"])
                self.assertEqual(updated["checkpoints"], original["checkpoints"])
                self.assertEqual(updated["channel_publications"]["workflow"]["status"], "not_started")
        self.assertEqual(progress, original)

    @staticmethod
    def progress():
        return {
            "current_checkpoint": "07",
            "checkpoints": [
                {"id": "07", "status": "passed"},
                {"id": "08", "status": "not_started"},
            ],
        }

    def test_route_is_offered_only_after_weather_release_passes(self):
        progress = self.progress()
        progress["checkpoints"][0]["status"] = "in_progress"
        self.assertEqual(route_after_weather_release(progress), "07")
        self.assertEqual(route_after_weather_release(self.progress()), "offer-weather-delivery")

    def test_skip_goes_directly_to_cultural_checkpoint(self):
        progress = choose_weather_delivery(self.progress(), "skip")
        self.assertEqual(route_after_weather_release(progress), "08")
        self.assertEqual(progress["current_checkpoint"], "08")
        self.assertEqual(progress["checkpoints"][1]["status"], "not_started")

    def test_optional_lab_completion_returns_to_checkpoint_08(self):
        progress = choose_weather_delivery(self.progress(), "start")
        for stage in ("capture", "review", "validate"):
            progress = advance_weather_delivery(progress, stage, "passed")
        progress = advance_weather_delivery(progress, "release", "passed")
        self.assertEqual(route_after_weather_release(progress), "08")
        self.assertEqual(progress["current_checkpoint"], "08")
        self.assertEqual(len(progress["optional_labs"]["weather_delivery"]["attempts"]), 4)

    def test_pause_resumes_at_same_stage_without_touching_core(self):
        progress = choose_weather_delivery(self.progress(), "start")
        progress = advance_weather_delivery(progress, "capture", "paused")
        self.assertEqual(route_after_weather_release(progress), "weather-delivery")
        self.assertEqual(progress["current_checkpoint"], "07")
        self.assertEqual(progress["optional_labs"]["weather_delivery"]["current_stage"], "capture")
        self.assertTrue(all(
            item["status"] == "not_started" for item in progress["checkpoints"][1:]
        ))

    def test_blocked_optional_lab_does_not_pass_core_or_auto_skip(self):
        progress = choose_weather_delivery(self.progress(), "start")
        progress = advance_weather_delivery(progress, "capture", "passed")
        progress = advance_weather_delivery(progress, "review", "passed")
        progress = advance_weather_delivery(progress, "validate", "blocked")
        self.assertEqual(route_after_weather_release(progress), "weather-delivery-blocked")
        self.assertEqual(progress["checkpoints"][0]["status"], "passed")
        self.assertEqual(progress["checkpoints"][1]["status"], "not_started")
        progress = skip_blocked_weather_delivery(progress)
        self.assertEqual(route_after_weather_release(progress), "08")
        self.assertEqual(progress["current_checkpoint"], "08")
        self.assertEqual(len(progress["optional_labs"]["weather_delivery"]["attempts"]), 3)

    def test_existing_progress_already_at_08_is_not_backtracked(self):
        progress = self.progress()
        progress["current_checkpoint"] = "08"
        self.assertEqual(route_after_weather_release(progress), "08")


class CiRecordTests(unittest.TestCase):
    def test_ci_record_contains_hashes_not_configuration_content(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "missing-manifest.json"
            output_path = Path(directory) / "record.json"
            record = write_ci_record("1" * 40, manifest_path, output_path)
            self.assertEqual(record["status"], "contract-suite-only")
            self.assertIsNone(record["manifest_sha256"])
            self.assertEqual(record["cases_sha256"], validation_cases_sha256())
            self.assertNotIn("toolbox", output_path.read_text(encoding="utf-8"))

    def test_ci_record_validates_capture_package_without_copying_configuration(self):
        import json
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            definition_path = root / "agent-definition.json"
            manifest_path = root / "manifest.json"
            output_path = root / "record.json"
            definition = captured_definition()
            definition_bytes = json.dumps(
                definition, ensure_ascii=False, sort_keys=True,
            ).encode("utf-8")
            definition_path.write_bytes(definition_bytes)
            config = capture_manifest()
            config["definition_sha256"] = hashlib.sha256(definition_bytes).hexdigest()
            manifest_path.write_text(json.dumps(config), encoding="utf-8")

            record = write_ci_record("1" * 40, manifest_path, output_path)

            self.assertEqual(record["status"], "capture-package-passed")
            self.assertEqual(record["manifest_sha256"], canonical_sha256(config))
            self.assertNotIn("Weather instructions.", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
