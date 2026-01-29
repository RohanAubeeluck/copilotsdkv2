#!/usr/bin/env python3
"""
GitHub Copilot Chat Demo Application

This application demonstrates how to use the copilot-sdk v2 to send prompts
to GitHub Copilot Chat and receive responses.

Usage:
    python app.py "Your prompt here"
    
Environment Variables:
    GITHUB_TOKEN: Your GitHub OAuth token (recommended)
    
Note:
    If GITHUB_TOKEN is not set, the app will fall back to the placeholder
    token defined in copilot_sdk/auth.py (which must be replaced manually).
"""

import sys
from copilot_sdk import CopilotClient


def main():
    """Main application entrypoint."""
    # Check for command line arguments
    if len(sys.argv) < 2:
        print("Usage: python app.py \"Your prompt here\"")
        print()
        print("Example:")
        print('  python app.py "Explain what async/await does in Python"')
        print()
        print("Configuration:")
        print("  Set GITHUB_TOKEN environment variable with your GitHub OAuth token")
        print("  or update the GITHUB_TOKEN constant in copilot_sdk/auth.py")
        sys.exit(1)
    
    # Get the prompt from command line arguments
    prompt = " ".join(sys.argv[1:])
    
    print(f"Sending prompt to GitHub Copilot Chat: {prompt}")
    print("-" * 60)
    
    try:
        # Create Copilot client
        client = CopilotClient()
        
        # Send the chat message
        response = client.send_chat_message(prompt)
        
        # Extract and print the response text
        response_text = client.get_completion_text(response)
        
        print("Response from GitHub Copilot:")
        print("-" * 60)
        print(response_text)
        print("-" * 60)
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
