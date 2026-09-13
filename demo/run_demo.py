#!/usr/bin/env python3
"""Run the offline public demonstration."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from uav_agent_demo.executor import Dispatcher, MockBackend
from uav_agent_demo.planner import MockPlanner
from uav_agent_demo.schema.parser import parse_mission_response


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Run without an LLM or AirSim.")
    parser.add_argument(
        "--instruction",
        default="Send two UAVs to inspect the forest for a missing person.",
    )
    args = parser.parse_args()
    if not args.mock:
        parser.error("This MVP currently supports only --mock.")

    print(f"Natural-language instruction: {args.instruction}")
    response = MockPlanner().plan(args.instruction)
    raw = response.model_dump_json(indent=2)
    print("\n[MOCK LLM] Deterministic offline response (no API call):")
    print(raw)
    validated = parse_mission_response(raw)
    print("\n[VALIDATION] Mission plan accepted.")
    results = Dispatcher(MockBackend()).dispatch(validated.plan)
    print(f"\n[RESULT] {len(results)} UAV tasks simulated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

