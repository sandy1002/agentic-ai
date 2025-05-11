import unittest
from unittest.mock import patch, MagicMock
from app.graph import build_graph

class TestGraph(unittest.TestCase):
    @patch("app.graph.fetch_unseen_emails")
    def test_fetch_emails_node(self, mock_fetch_unseen_emails):
        # Mock the fetch_unseen_emails function
        mock_fetch_unseen_emails.return_value = [
            {"subject": "Test Email 1", "body": "Body of email 1"},
            {"subject": "Test Email 2", "body": "Body of email 2"},
        ]

        # Build the graph and execute the fetch_emails node
        graph = build_graph()
        state = graph.execute("fetch_emails", {"emails": [], "summaries": []})

        # Assertions
        self.assertEqual(len(state["emails"]), 2)
        self.assertEqual(state["emails"][0]["subject"], "Test Email 1")

    @patch("app.graph.summarize_email")
    def test_summarize_emails_node(self, mock_summarize_email):
        # Mock the summarize_email function
        mock_summarize_email.side_effect = lambda subject, body: f"Summary of {subject}"

        # Build the graph and execute the summarize_emails node
        graph = build_graph()
        state = {
            "emails": [
                {"subject": "Test Email 1", "body": "Body of email 1"},
                {"subject": "Test Email 2", "body": "Body of email 2"},
            ],
            "summaries": [],
        }
        state = graph.execute("summarize_emails", state)

        # Assertions
        self.assertEqual(len(state["summaries"]), 2)
        self.assertEqual(state["summaries"][0]["summary"], "Summary of Test Email 1")

    @patch("app.graph.add_email_to_memory")
    def test_store_in_memory_node(self, mock_add_email_to_memory):
        # Mock the add_email_to_memory function
        mock_add_email_to_memory.return_value = None

        # Build the graph and execute the store_in_memory node
        graph = build_graph()
        state = {
            "emails": [
                {"subject": "Test Email 1", "body": "Body of email 1"},
                {"subject": "Test Email 2", "body": "Body of email 2"},
            ],
            "summaries": [],
        }
        state = graph.execute("store_in_memory", state)

        # Assertions
        self.assertEqual(mock_add_email_to_memory.call_count, 2)
        mock_add_email_to_memory.assert_any_call("Test Email 1", "Body of email 1")
        mock_add_email_to_memory.assert_any_call("Test Email 2", "Body of email 2")

    def test_graph_execution_flow(self):
        # Mock dependencies for the entire graph
        with patch("app.graph.fetch_unseen_emails") as mock_fetch_emails, \
             patch("app.graph.summarize_email") as mock_summarize_email, \
             patch("app.graph.add_email_to_memory") as mock_add_email_to_memory:

            # Mock return values
            mock_fetch_emails.return_value = [
                {"subject": "Test Email 1", "body": "Body of email 1"},
                {"subject": "Test Email 2", "body": "Body of email 2"},
            ]
            mock_summarize_email.side_effect = lambda subject, body: f"Summary of {subject}"
            mock_add_email_to_memory.return_value = None

            # Build the graph and execute it
            graph = build_graph()
            state = graph.execute("fetch_emails", {"emails": [], "summaries": []})
            state = graph.execute("summarize_emails", state)
            state = graph.execute("store_in_memory", state)

            # Assertions
            self.assertEqual(len(state["emails"]), 2)
            self.assertEqual(len(state["summaries"]), 2)
            self.assertEqual(state["summaries"][0]["summary"], "Summary of Test Email 1")
            self.assertEqual(mock_add_email_to_memory.call_count, 2)

if __name__ == "__main__":
    unittest.main()