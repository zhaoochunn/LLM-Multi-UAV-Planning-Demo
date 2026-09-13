"""Deterministic offline planner used by the public demo."""

from __future__ import annotations

from typing import Any

from uav_agent_demo.schema import MissionResponse


def _task(
    uav_id: str, role: str, movement: str, heading: float | None,
    pattern: str, area: str, target: str, altitude: float,
) -> dict[str, Any]:
    return {
        "uav_id": uav_id, "role": role, "execution_mode": "DIRECT",
        "horizontal_movement": movement, "heading": heading,
        "vertical_movement": "LEVEL", "search_pattern": pattern,
        "priority_target": target, "speed": 2.0, "altitude": altitude,
        "target_area": area, "constraints": {},
    }


class MockPlanner:
    """Return one fixture; the instruction is recorded but not interpreted."""

    def plan(self, instruction: str) -> MissionResponse:
        return MissionResponse.model_validate({
            "reasoning": {
                "scene_summary": instruction,
                "allocation_logic": "Assign two search sectors and keep UAV_00 as relay.",
                "tradeoffs": "Static sectors demonstrate dispatch without adaptive replanning.",
                "confidence": "HIGH",
            },
            "plan": {
                "mission_name": "offline-forest-search", "scene_type": "RADIAL",
                "uav_count": 3, "target_count": 1,
                "tasks": [
                    _task("UAV_00", "RELAY_STATION", "STAY", None, "STAY", "relay standby", "none", 100),
                    _task("UAV_01", "SEARCHER", "HEADING", 0, "RADIAL", "sector A", "person", 50),
                    _task("UAV_02", "SEARCHER", "HEADING", 180, "RADIAL", "sector B", "person", 50),
                ],
                "global_constraints": "Validate the plan before dispatch.",
            },
        })
