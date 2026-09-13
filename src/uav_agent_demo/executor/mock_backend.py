"""Offline UAV backend that records, but does not perform, actions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionResult:
    uav_id: str
    action: str
    status: str = "SIMULATED"


class MockBackend:
    def execute(self, uav_id: str, action: str) -> ExecutionResult:
        print(f"[MOCK UAV EXECUTION] {uav_id}: {action}")
        return ExecutionResult(uav_id=uav_id, action=action)

