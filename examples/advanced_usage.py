#!/usr/bin/env python3
"""
Advanced example showing how to use the Copilot SDK programmatically.

This example demonstrates:
- Creating a client with custom configuration
- Handling multiple prompts
- Error handling
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from copilot_sdk import CopilotClient


def main():
    """Demonstrate advanced SDK usage."""
    
    # Example prompts
    prompts = [
        "What is a Python decorator?",
        "Explain list comprehensions",
        "How does garbage collection work in Python?"
    ]
    
    try:
        # Create client (token from environment or placeholder)
        client = CopilotClient()
        
        print("GitHub Copilot SDK - Advanced Example")
        print("=" * 60)
        
        # Process each prompt
        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{len(prompts)}] Sending: {prompt}")
            print("-" * 60)
            
            # Send prompt
            response = client.send_chat_message(prompt)
            
            # Extract response
            text = client.get_completion_text(response)
            
            # Print response (truncated for demo)
            lines = text.split('\n')
            preview = '\n'.join(lines[:5])
            if len(lines) > 5:
                preview += f"\n... ({len(lines) - 5} more lines)"
            
            print(preview)
            print("-" * 60)
        
        print("\nAll prompts processed successfully!")
        
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nTo run this example, set GITHUB_TOKEN environment variable:")
        print("  export GITHUB_TOKEN='your_github_token_here'")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
