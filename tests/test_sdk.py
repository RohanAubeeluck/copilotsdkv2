"""Tests for the copilot_sdk package."""

import unittest
from unittest.mock import patch, Mock
from copilot_sdk import CopilotClient, get_copilot_token
from copilot_sdk.auth import GITHUB_TOKEN


class TestAuth(unittest.TestCase):
    """Test authentication functionality."""
    
    def test_placeholder_token_raises_error(self):
        """Test that using placeholder token raises a clear error."""
        with self.assertRaises(ValueError) as context:
            get_copilot_token()
        
        self.assertIn("GitHub token not configured", str(context.exception))
    
    @patch('copilot_sdk.auth.os.getenv')
    def test_environment_variable_used(self, mock_getenv):
        """Test that environment variable is preferred over placeholder."""
        mock_getenv.return_value = "test_token_from_env"
        
        with patch('copilot_sdk.auth.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"token": "copilot_token_123"}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            token = get_copilot_token()
            
            # Verify the request was made with the env token
            mock_get.assert_called_once()
            call_kwargs = mock_get.call_args[1]
            self.assertIn("authorization", call_kwargs["headers"])
            self.assertIn("test_token_from_env", call_kwargs["headers"]["authorization"])


class TestClient(unittest.TestCase):
    """Test client functionality."""
    
    def test_client_initialization(self):
        """Test that client can be initialized."""
        client = CopilotClient(github_token="test_token")
        self.assertEqual(client.github_token, "test_token")
        self.assertIsNone(client.copilot_token)
    
    @patch('copilot_sdk.client.get_copilot_token')
    @patch('copilot_sdk.client.requests.post')
    def test_send_chat_message(self, mock_post, mock_get_token):
        """Test sending a chat message."""
        mock_get_token.return_value = "copilot_bearer_token"
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "Hello from Copilot!"}}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = CopilotClient(github_token="test_token")
        response = client.send_chat_message("Hello")
        
        self.assertIn("choices", response)
        self.assertEqual(
            client.get_completion_text(response),
            "Hello from Copilot!"
        )


if __name__ == "__main__":
    unittest.main()
