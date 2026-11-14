import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

MODULE7_PATH = Path(r"C:\playwright-project\module7-scheduler")
sys.path.insert(0, str(MODULE7_PATH))

from scheduler import Scheduler


class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.task_queue = MagicMock()
        self.scheduler = Scheduler(self.task_queue)
        self.task = "Test Task"

    def test_run_immediately(self):
        self.task_queue.add_task.return_value = "Added"

        result = self.scheduler.run_immediately(self.task)

        self.task_queue.add_task.assert_called_once_with(self.task)
        self.assertEqual(result, "Added")

    @patch("scheduler.threading.Timer")
    def test_run_after_delay(self, mock_timer):
        timer = MagicMock()
        mock_timer.return_value = timer

        result = self.scheduler.run_after_delay(
            self.task, 5
        )

        mock_timer.assert_called_once()
        timer.start.assert_called_once()
        self.assertIs(result, timer)

    @patch("scheduler.threading.Timer")
    def test_run_every(self, mock_timer):
        self.scheduler.run_every(
            lambda: self.task, 1
        )

        self.task_queue.add_task.assert_called_once_with(
            self.task
        )
        self.assertTrue(self.scheduler.running)
        mock_timer.return_value.start.assert_called_once()

    @patch("scheduler.threading.Timer")
    def test_run_daily(self, mock_timer):
        self.scheduler.run_daily(
            lambda: self.task, 10, 30
        )

        self.assertTrue(self.scheduler.running)
        mock_timer.return_value.start.assert_called_once()

    @patch("scheduler.threading.Timer")
    def test_run_weekly(self, mock_timer):
        self.scheduler.run_weekly(
            lambda: self.task, 0, 10, 30
        )

        self.assertTrue(self.scheduler.running)
        mock_timer.return_value.start.assert_called_once()

    @patch("scheduler.threading.Timer")
    def test_stop_scheduler(self, mock_timer):
        self.scheduler.run_after_delay(self.task, 5)

        self.scheduler.stop()

        self.assertFalse(self.scheduler.running)
        mock_timer.return_value.cancel.assert_called_once()
        self.assertEqual(self.scheduler.timers, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
    