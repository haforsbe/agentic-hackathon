"""One non-secret configuration contract for the host and reference workflow."""

from dataclasses import asdict, dataclass
import json
import os
import re
from typing import Mapping
from urllib.parse import urlsplit
from uuid import UUID


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class SpecialistConfig:
    agent_name: str
    version: str
    server_label: str
    tool_name: str


@dataclass(frozen=True)
class WorkflowConfig:
    project_endpoint: str
    tenant_id: str
    runtime_principal_id: str
    workflow_name: str
    weather: SpecialistConfig
    culture: SpecialistConfig


def _object(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ConfigurationError(f"{label} must contain exactly the documented fields")
    return value


def _string(value, pattern, label):
    if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
        raise ConfigurationError(f"Invalid {label}; use a confirmed resource value")
    return value


def _uuid(value, label):
    if not isinstance(value, str):
        raise ConfigurationError(f"Invalid {label}; expected a UUID")
    try:
        parsed = UUID(value)
    except ValueError:
        raise ConfigurationError(f"Invalid {label}; expected a UUID") from None
    if str(parsed) != value or not parsed.int:
        raise ConfigurationError(f"Invalid {label}; expected a canonical nonzero UUID")
    return value


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ConfigurationError("Duplicate configuration fields are not supported")
        value[key] = item
    return value


def load_config(environ: Mapping[str, str] | None = None) -> WorkflowConfig:
    environment = os.environ if environ is None else environ
    raw = environment.get("WORKFLOW_CONFIG_JSON")
    if not raw:
        raise ConfigurationError(
            "WORKFLOW_CONFIG_JSON is required; complete and confirm config.example.json first"
        )
    try:
        value = json.loads(raw, object_pairs_hook=_unique_object)
    except (TypeError, json.JSONDecodeError):
        raise ConfigurationError("WORKFLOW_CONFIG_JSON must be a JSON object") from None
    value = _object(value, (
        "participant_confirmed", "project_endpoint", "tenant_id", "runtime_principal_id",
        "workflow_name", "weather", "culture",
    ), "Workflow configuration")
    if value["participant_confirmed"] is not True:
        raise ConfigurationError("Participant confirmation is required before runtime startup")
    endpoint = value["project_endpoint"]
    if not isinstance(endpoint, str):
        raise ConfigurationError("Invalid project_endpoint")
    try:
        parsed = urlsplit(endpoint)
        valid_endpoint = (
            parsed.scheme == "https"
            and re.fullmatch(r"[a-z0-9][a-z0-9-]*\.services\.ai\.azure\.com", parsed.netloc)
            and re.fullmatch(r"/api/projects/[A-Za-z0-9_-]+", parsed.path)
            and not parsed.query and not parsed.fragment
        )
    except ValueError:
        valid_endpoint = False
    if not valid_endpoint:
        raise ConfigurationError("project_endpoint must be the exact HTTPS Microsoft Foundry Project Endpoint")
    name_pattern = r"[A-Za-z][A-Za-z0-9_-]{0,62}"

    def specialist(domain):
        fields = _object(value[domain], ("agent_name", "version", "server_label", "tool_name"), domain)
        return SpecialistConfig(
            _string(fields["agent_name"], name_pattern, f"{domain}.agent_name"),
            _string(fields["version"], r"[1-9][0-9]*", f"{domain}.version"),
            _string(fields["server_label"], r"[A-Za-z0-9_-]{1,128}", f"{domain}.server_label"),
            _string(fields["tool_name"], r"[A-Za-z0-9_.-]{1,128}", f"{domain}.tool_name"),
        )

    config = WorkflowConfig(
        endpoint, _uuid(value["tenant_id"], "tenant_id"),
        _uuid(value["runtime_principal_id"], "runtime_principal_id"),
        _string(value["workflow_name"], name_pattern, "workflow_name"),
        specialist("weather"), specialist("culture"),
    )
    if len({config.workflow_name, config.weather.agent_name, config.culture.agent_name}) != 3:
        raise ConfigurationError("The workflow and both specialists must be distinct agents")
    return config


def manifest(config: WorkflowConfig) -> str:
    """Render local deployment plumbing from the same confirmed configuration."""
    setting = json.dumps(json.dumps({"participant_confirmed": True, **asdict(config)}))
    return f"""# Generated locally from WORKFLOW_CONFIG_JSON; never commit this configured file.
name: {config.workflow_name}
infra:
  provider: microsoft.foundry
requiredVersions:
  azd: '>=1.27.1'
  extensions:
    azure.ai.agents: '>=1.0.0-beta.9'
services:
  ai-project:
    host: azure.ai.project
    endpoint: {config.project_endpoint}
    deployments: []
  workflow:
    name: {config.workflow_name}
    host: azure.ai.agent
    kind: hosted
    language: python
    project: src
    description: Reference graph with independently approved specialist evidence.
    codeConfiguration:
      dependencyResolution: remote_build
      entryPoint: trip_server.py
      runtime: python_3_13
    container:
      resources:
        cpu: "0.5"
        memory: 1Gi
    env:
      PYTHONNOUSERSITE: "1"
      WORKFLOW_CONFIG_JSON: {setting}
    protocols:
      - protocol: responses
        version: 2.0.0
      - protocol: invocations
        version: 2.0.0
    uses:
      - ai-project
"""


if __name__ == "__main__":
    print(manifest(load_config()), end="")
