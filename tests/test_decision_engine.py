import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

MODULE9_PATH = Path(r"C:\playwright-project\module9-llm-integration")
sys.path.insert(0, str(MODULE9_PATH))

from decision_engine import DecisionEngine


class TestDecisionEngine(unittest.TestCase):

    def setUp(self):
        with patch("decision_engine.PlanningEngine") as planner, \
             patch("decision_engine.ToolSelector") as selector, \
             patch("decision_engine.ReflectionEngine") as reflection:

            self.engine = DecisionEngine()

            self.engine.planner = planner.return_value
            self.engine.tool_selector = selector.return_value
            self.engine.reflection = reflection.return_value

    def test_initialization(self):
        self.assertIsNotNone(self.engine.planner)
        self.assertIsNotNone(self.engine.tool_selector)
        self.assertIsNotNone(self.engine.reflection)
        self.assertEqual(self.engine.decision_history, [])

    def test_analyze_objective(self):
        objective = "Open a website and read its content"

        self.engine.planner.generate_plan.return_value = [
            {"task_id": "T001", "task": "Open website"}
        ]

        self.engine.tool_selector.select_tools_for_plan.return_value = [
            {
                "task_id": "T001",
                "task": "Open website",
                "selected_tool": "browser"
            }
        ]

        result = self.engine.analyze_objective(objective)

        self.assertEqual(result["objective"], objective)
        self.assertEqual(result["status"], "decision_ready")
        self.assertEqual(len(result["decisions"]), 1)
        self.assertEqual(
            result["decisions"][0]["selected_tool"],
            "browser"
        )

    def test_handle_failure(self):
        self.engine.reflection.recover.return_value = {
            "status": "recovery_ready"
        }

        result = self.engine.handle_failure(
            "T001", "Browser error"
        )

        self.engine.reflection.recover.assert_called_once()

        self.assertEqual(
            result["status"],
            "recovery_ready"
        )

    def test_decision_history(self):
        self.engine.decision_history.append({
            "objective": "Test objective",
            "status": "decision_ready"
        })

        history = self.engine.get_decision_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(
            history[0]["objective"],
            "Test objective"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)