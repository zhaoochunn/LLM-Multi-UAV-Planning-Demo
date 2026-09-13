"""Map validated UAV tasks to backend actions."""

from uav_agent_demo.executor.mock_backend import ExecutionResult, MockBackend
from uav_agent_demo.schema import MissionPlan, UAVTask


class Dispatcher:
    def __init__(self, backend: MockBackend) -> None:
        self.backend = backend

    def dispatch(self, plan: MissionPlan) -> list[ExecutionResult]:
        return [self.backend.execute(task.uav_id, self._action_for(task)) for task in plan.tasks]

    @staticmethod
    def _action_for(task: UAVTask) -> str:
        if task.role == "RELAY_STATION":
            return f"hold relay position at {task.altitude:.0f} m"
        return (
            f"search {task.target_area} using {task.search_pattern} "
            f"at heading {task.heading:.0f} degrees"
        )

