"""Authentication module for GitHub Copilot SDK."""

import os
import requests


# Placeholder token - DO NOT use a real token here
# Replace this with your actual GitHub token or set GITHUB_TOKEN environment variable
GITHUB_TOKEN = "REPLACE_ME"


def get_copilot_token(github_token=None):
    """
    Get a Copilot-specific bearer token from GitHub.
    
    This function exchanges a GitHub OAuth token for a Copilot-specific token
    that can be used to interact with the Copilot API.
    
    Args:
        github_token (str, optional): GitHub OAuth token. If not provided,
                                     will check GITHUB_TOKEN env var, then
                                     fall back to the placeholder constant.
    
    Returns:
        str: Copilot bearer token
        
    Raises:
        Exception: If token exchange fails
    """
    # Priority: parameter > environment variable > hardcoded placeholder
    token = github_token or os.getenv("GITHUB_TOKEN") or GITHUB_TOKEN
    
    if token == "REPLACE_ME":
        raise ValueError(
            "GitHub token not configured. Please either:\n"
            "1. Set GITHUB_TOKEN environment variable, or\n"
            "2. Pass token as parameter to get_copilot_token(), or\n"
            "3. Update GITHUB_TOKEN constant in copilot_sdk/auth.py"
        )
    
    # Exchange GitHub token for Copilot token
    headers = {
        "authorization": f"token {token}",
        "editor-version": "vscode/1.85.1",
        "editor-plugin-version": "copilot/1.155.0",
        "user-agent": "GitHubCopilot/1.155.0"
    }
    
    try:
        response = requests.get(
            "https://api.github.com/copilot_internal/v2/token",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()["token"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get Copilot token: {e}")
    except KeyError:
        raise Exception("Unexpected response format from Copilot token API")
