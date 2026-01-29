#!/usr/bin/env python3
"""
Simple example showing basic SDK usage as a library.

This demonstrates the minimal code needed to use the SDK.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from copilot_sdk import CopilotClient


def ask_copilot(question):
    """
    Ask GitHub Copilot a question and return the answer.
    
    Args:
        question (str): The question to ask
        
    Returns:
        str: Copilot's response
    """
    client = CopilotClient()
    response = client.send_chat_message(question)
    return client.get_completion_text(response)


def main():
    """Simple demo of the SDK."""
    try:
        # Ask Copilot a question
        question = "What is the Zen of Python?"
        print(f"Question: {question}\n")
        
        answer = ask_copilot(question)
        print(f"Answer:\n{answer}")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease set GITHUB_TOKEN environment variable")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
