import time
import psutil
import threading

from datetime import datetime


class SystemMonitor:

    def __init__(self):

        self.start_time = time.time()

        self.agents = {}
        self.browsers = {}

        self.running_tasks = 0
        self.completed_tasks = 0
        self.failed_tasks = 0

        self.lock = threading.Lock()

        print("System Monitor Initialized")

    # Agent Monitoring
    def register_agent(self, agent_id, status="active"):

        with self.lock:

            self.agents[agent_id] = {
                "status": status,
                "last_updated": datetime.now().isoformat()
            }

        print(f"Agent Registered: {agent_id}")

    def update_agent_status(self, agent_id, status):

        with self.lock:

            if agent_id in self.agents:

                self.agents[agent_id]["status"] = status

                self.agents[agent_id]["last_updated"] = (
                    datetime.now().isoformat()
                )

        print(f"Agent Status Updated: {agent_id} -> {status}")

    # Browser Monitoring
    def register_browser(self, browser_id, status="running"):

        with self.lock:

            self.browsers[browser_id] = status

        print(f"Browser Registered: {browser_id}")

    def update_browser_status(self, browser_id, status):

        with self.lock:

            if browser_id in self.browsers:

                self.browsers[browser_id] = status

        print(f"Browser Status Updated: {browser_id} -> {status}")

    # Task Monitoring
    def task_started(self):

        with self.lock:

            self.running_tasks += 1

        print("Task Started")

    def task_completed(self):

        with self.lock:

            self.running_tasks = max(0, self.running_tasks - 1)
            self.completed_tasks += 1

        print("Task Completed")

    def task_failed(self):

        with self.lock:

            self.running_tasks = max(0, self.running_tasks - 1)
            self.failed_tasks += 1

        print("Task Failed")

    # CPU Monitoring
    def get_cpu_usage(self):

        return psutil.cpu_percent(interval=1)

    # Memory Monitoring
    def get_memory_usage(self):

        memory = psutil.virtual_memory()

        return {
            "total_mb": round(memory.total / (1024 * 1024), 2),
            "used_mb": round(memory.used / (1024 * 1024), 2),
            "available_mb": round(memory.available / (1024 * 1024), 2),
            "percentage": memory.percent
        }

    # Execution Time
    def get_execution_time(self):

        return round(time.time() - self.start_time, 2)

    # Complete System Report
    def get_system_report(self):

        with self.lock:

            agents = self.agents.copy()
            browsers = self.browsers.copy()

            running = self.running_tasks
            completed = self.completed_tasks
            failed = self.failed_tasks

        return {
            "agents": agents,
            "browsers": browsers,
            "running_tasks": running,
            "completed_tasks": completed,
            "failed_tasks": failed,
            "cpu_usage": self.get_cpu_usage(),
            "memory_usage": self.get_memory_usage(),
            "execution_time": self.get_execution_time()
        }

    def display_report(self):

        report = self.get_system_report()

        print("\n========== SYSTEM MONITORING REPORT ==========")

        print("\nAgent Status:")
        print(report["agents"])

        print("\nBrowser Status:")
        print(report["browsers"])

        print("\nTask Statistics:")
        print("Running:", report["running_tasks"])
        print("Completed:", report["completed_tasks"])
        print("Failed:", report["failed_tasks"])

        print("\nPerformance:")
        print("CPU Usage:", report["cpu_usage"], "%")
        print("Memory Usage:", report["memory_usage"])
        print("Execution Time:", report["execution_time"], "seconds")

        print("\n========== REPORT COMPLETED ==========")


monitor = SystemMonitor()