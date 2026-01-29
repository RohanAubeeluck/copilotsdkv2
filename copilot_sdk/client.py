"""Client module for GitHub Copilot Chat API interactions."""

import requests
from .auth import get_copilot_token


class CopilotClient:
    """Client for interacting with GitHub Copilot Chat API."""
    
    def __init__(self, github_token=None):
        """
        Initialize the Copilot client.
        
        Args:
            github_token (str, optional): GitHub OAuth token. If not provided,
                                         will use environment variable or placeholder.
        """
        self.github_token = github_token
        self.copilot_token = None
        self.base_url = "https://api.githubcopilot.com"
    
    def authenticate(self):
        """Authenticate and get a Copilot bearer token."""
        self.copilot_token = get_copilot_token(self.github_token)
        return self.copilot_token
    
    def send_chat_message(self, prompt, model="gpt-4"):
        """
        Send a chat message to GitHub Copilot.
        
        Args:
            prompt (str): The prompt/message to send
            model (str): The model to use (default: gpt-4)
        
        Returns:
            dict: Response from the Copilot API
            
        Raises:
            Exception: If the API request fails
        """
        if not self.copilot_token:
            self.authenticate()
        
        headers = {
            "Authorization": f"Bearer {self.copilot_token}",
            "Content-Type": "application/json",
            "User-Agent": "GitHubCopilot/1.155.0",
            "Editor-Version": "vscode/1.85.1",
            "Copilot-Integration-Id": "vscode-chat"
        }
        
        # Use chat completions endpoint
        url = f"{self.base_url}/chat/completions"
        
        data = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send chat message: {e}")
    
    def get_completion_text(self, response):
        """
        Extract the completion text from API response.
        
        Args:
            response (dict): API response from send_chat_message
            
        Returns:
            str: The completion text
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return str(response)
