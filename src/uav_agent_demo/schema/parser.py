"""Parse untrusted planner text into the validated mission contract."""

import json

from .mission import MissionResponse


def parse_mission_response(raw_output: str) -> MissionResponse:
    """Parse JSON and reject any payload that violates the mission schema."""
    payload = json.loads(raw_output)
    return MissionResponse.model_validate(payload)

