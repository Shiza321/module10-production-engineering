import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PerformanceManager")


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start
        logger.info("%s completed in %.4f seconds", func.__name__, elapsed)

        return result

    return wrapper


class PerformanceManager:

    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        logger.info("Performance Manager Initialized")

    @measure_time
    def execute_task(self, task):
        return task()

    def execute_parallel(self, tasks):
        results = []

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futures = [
                executor.submit(task)
                for task in tasks
            ]

            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as error:
                    logger.error("Task failed: %s", error)

        return results

    def get_worker_limit(self):
        return self.max_workers


if __name__ == "__main__":

    manager = PerformanceManager(max_workers=3)

    tasks = [
        lambda: "Task 1 completed",
        lambda: "Task 2 completed",
        lambda: "Task 3 completed",
    ]

    print("\nExecuting Tasks in Parallel")

    results = manager.execute_parallel(tasks)

    for result in results:
        print(result)

    print("\nMaximum Workers:", manager.get_worker_limit())
    print("\nPERFORMANCE TEST COMPLETED")