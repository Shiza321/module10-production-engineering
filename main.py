from config.settings import settings
from monitoring.logger import logger
from monitoring.monitor import monitor


def main():

    print("\n========== MODULE 10 TASK 2 ==========")

    # Logger Testing
    print("\n[1] Testing Production Logger")

    logger.info("Production Framework Started")
    logger.warning("Monitoring System Active")
    logger.info("Logger Test Successful")

    # Agent Monitoring
    print("\n[2] Testing Agent Monitoring")

    monitor.register_agent("A001", "active")
    monitor.register_agent("A002", "active")

    monitor.update_agent_status("A002", "busy")

    # Browser Monitoring
    print("\n[3] Testing Browser Monitoring")

    monitor.register_browser("B001", "running")
    monitor.update_browser_status("B001", "active")

    # Task Monitoring
    print("\n[4] Testing Task Monitoring")

    monitor.task_started()
    monitor.task_completed()

    monitor.task_started()
    monitor.task_failed()

    # System Performance
    print("\n[5] Testing CPU and Memory Monitoring")

    # Complete Monitoring Report
    print("\n[6] Generating System Report")

    monitor.display_report()

    logger.info("Monitoring Test Completed")

    print("\n========== TASK 2 COMPLETED ==========")


if __name__ == "__main__":
    main()