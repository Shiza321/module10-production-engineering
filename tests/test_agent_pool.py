import sys
import unittest
from pathlib import Path

MODULE8_PATH = Path(r"C:\playwright-project\module8-multi-agent")
sys.path.insert(0, str(MODULE8_PATH))

from agent_pool import AgentPool, AgentState


class TestAgentPool(unittest.TestCase):

    def setUp(self):
        self.pool = AgentPool()

    def test_create_agent(self):
        agent = self.pool.create_agent("A001", "Browser Agent")

        self.assertIsNotNone(agent)
        self.assertEqual(agent.state, AgentState.CREATED)

    def test_register_agent(self):
        agent = self.pool.create_agent("A001", "Browser Agent")

        result = self.pool.register_agent(agent)

        self.assertTrue(result)
        self.assertEqual(agent.state, AgentState.REGISTERED)

    def test_activate_agent(self):
        agent = self.pool.create_agent("A001", "Browser Agent")
        self.pool.register_agent(agent)

        result = self.pool.activate_agent("A001")

        self.assertTrue(result)
        self.assertEqual(agent.state, AgentState.AVAILABLE)

    def test_deactivate_agent(self):
        agent = self.pool.create_agent("A001", "Browser Agent")
        self.pool.register_agent(agent)
        self.pool.activate_agent("A001")

        result = self.pool.deactivate_agent("A001")

        self.assertTrue(result)
        self.assertEqual(agent.state, AgentState.INACTIVE)

    def test_remove_agent(self):
        agent = self.pool.create_agent("A001", "Browser Agent")
        self.pool.register_agent(agent)

        result = self.pool.remove_agent("A001")

        self.assertTrue(result)
        self.assertNotIn("A001", self.pool.agents)
        self.assertEqual(agent.state, AgentState.REMOVED)

    def test_get_available_agents(self):
        agent = self.pool.create_agent("A001", "Browser Agent")
        self.pool.register_agent(agent)
        self.pool.activate_agent("A001")

        available = self.pool.get_available_agents()

        self.assertEqual(len(available), 1)
        self.assertEqual(available[0].agent_id, "A001")

    def test_duplicate_agent_registration(self):
        agent = self.pool.create_agent("A001", "Browser Agent")
        self.pool.register_agent(agent)

        result = self.pool.register_agent(agent)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)