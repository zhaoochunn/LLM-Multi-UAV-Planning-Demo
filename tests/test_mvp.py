import pytest
from pydantic import ValidationError

from uav_agent_demo.executor import Dispatcher, MockBackend
from uav_agent_demo.planner import MockPlanner
from uav_agent_demo.schema.parser import parse_mission_response


def test_mock_plan_parses_and_dispatches_all_uavs():
    plan = MockPlanner().plan("Search the forest.")
    parsed = parse_mission_response(plan.model_dump_json())
    results = Dispatcher(MockBackend()).dispatch(parsed.plan)
    assert [result.uav_id for result in results] == ["UAV_00", "UAV_01", "UAV_02"]
    assert all(result.status == "SIMULATED" for result in results)


def test_malformed_task_is_rejected():
    plan = MockPlanner().plan("Search the forest.").model_dump()
    plan["plan"]["tasks"][1]["uav_id"] = "drone-one"
    with pytest.raises(ValidationError):
        parse_mission_response(__import__("json").dumps(plan))


def test_stay_task_with_heading_is_rejected():
    plan = MockPlanner().plan("Ignored fixture input.").model_dump()
    plan["plan"]["tasks"][0]["heading"] = 90
    with pytest.raises(ValidationError):
        parse_mission_response(__import__("json").dumps(plan))


def test_duplicate_uav_ids_are_rejected():
    plan = MockPlanner().plan("Ignored fixture input.").model_dump()
    plan["plan"]["tasks"][2]["uav_id"] = "UAV_01"
    with pytest.raises(ValidationError):
        parse_mission_response(__import__("json").dumps(plan))


def test_relay_must_be_uav_00():
    plan = MockPlanner().plan("Ignored fixture input.").model_dump()
    plan["plan"]["tasks"][0]["role"] = "SEARCHER"
    plan["plan"]["tasks"][1]["role"] = "RELAY_STATION"
    with pytest.raises(ValidationError):
        parse_mission_response(__import__("json").dumps(plan))
