"""
Basic usage example of CopilotPrompt.

This example demonstrates the simplest way to use the CopilotPrompt class
to send a prompt and receive a response.
"""

import asyncio
from copilotsdkv2 import CopilotPrompt


async def main():
    """Main function demonstrating basic usage."""
    # Create a CopilotPrompt instance
    prompt = CopilotPrompt()

    try:
        # Start the client
        print("Starting Copilot client...")
        await prompt.start()
        print("Client started successfully!")

        # Send a prompt and get response
        print("\nSending prompt: 'What is 2+2?'")
        response = await prompt.send_prompt("What is 2+2?")
        print(f"\nResponse: {response}")

        # Send another prompt
        print("\nSending prompt: 'Explain Python in one sentence'")
        response = await prompt.send_prompt("Explain Python in one sentence")
        print(f"\nResponse: {response}")

    finally:
        # Clean up
        print("\nStopping client...")
        await prompt.stop()
        print("Client stopped.")


if __name__ == "__main__":
    asyncio.run(main())
