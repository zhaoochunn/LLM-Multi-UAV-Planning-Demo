"""Validated data contract between planning and execution."""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UAVTask(StrictModel):
    uav_id: str = Field(pattern=r"^UAV_\d{2}$")
    role: Literal["SEARCHER", "RELAY_STATION"]
    execution_mode: Literal["DIRECT"] = "DIRECT"
    horizontal_movement: Literal["HEADING", "STAY"]
    heading: Optional[float] = Field(default=None, ge=0, le=360)
    vertical_movement: Literal["CLIMB", "DESCEND", "LEVEL"] = "LEVEL"
    search_pattern: Literal["GRID", "S-SCAN", "RADIAL", "STAY"]
    priority_target: str
    speed: float = Field(gt=0, le=20)
    altitude: float = Field(ge=20, le=120)
    target_area: str = Field(min_length=1)
    constraints: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def movement_is_consistent(self) -> "UAVTask":
        staying = self.horizontal_movement == "STAY" or self.search_pattern == "STAY"
        if staying and not (
            self.horizontal_movement == "STAY"
            and self.search_pattern == "STAY"
            and self.heading is None
        ):
            raise ValueError("STAY requires STAY movement, STAY pattern, and null heading")
        if not staying and self.heading is None:
            raise ValueError("moving tasks require a heading")
        return self


class MissionPlan(StrictModel):
    mission_name: str = Field(min_length=1)
    scene_type: Literal["LINEAR", "RADIAL", "MULTI_ZONE", "URBAN"]
    uav_count: int = Field(ge=1, le=10)
    target_count: int = Field(ge=1)
    tasks: list[UAVTask] = Field(min_length=1)
    global_constraints: Optional[str] = None

    @model_validator(mode="after")
    def validate_swarm(self) -> "MissionPlan":
        ids = [task.uav_id for task in self.tasks]
        if self.uav_count != len(self.tasks):
            raise ValueError("uav_count must equal the number of tasks")
        if len(ids) != len(set(ids)):
            raise ValueError("uav_id values must be unique")
        relays = [task for task in self.tasks if task.role == "RELAY_STATION"]
        if len(relays) != 1 or relays[0].uav_id != "UAV_00":
            raise ValueError("exactly one UAV_00 relay task is required")
        return self


class MissionReasoning(StrictModel):
    scene_summary: str
    allocation_logic: str
    tradeoffs: Optional[str] = None
    confidence: Literal["HIGH", "MEDIUM", "LOW"]


class MissionResponse(StrictModel):
    reasoning: MissionReasoning
    plan: MissionPlan
