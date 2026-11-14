import unittest
from performance import PerformanceManager


class TestPerformanceManager(unittest.TestCase):

    def setUp(self):
        self.manager = PerformanceManager(max_workers=3)

    def test_worker_limit(self):
        self.assertEqual(self.manager.get_worker_limit(), 3)

    def test_parallel_execution(self):
        tasks = [
            lambda: "Task 1",
            lambda: "Task 2",
            lambda: "Task 3"
        ]

        results = self.manager.execute_parallel(tasks)

        self.assertEqual(len(results), 3)
        self.assertCountEqual(
            results,
            ["Task 1", "Task 2", "Task 3"]
        )

    def test_empty_tasks(self):
        results = self.manager.execute_parallel([])
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()