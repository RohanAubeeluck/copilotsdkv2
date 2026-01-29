"""
Context manager example for CopilotPrompt.

This example demonstrates using CopilotPrompt with the async context manager
pattern, which automatically handles startup and cleanup.
"""

import asyncio
from copilotsdkv2 import CopilotPrompt


async def main():
    """Main function demonstrating context manager usage."""
    print("Using CopilotPrompt with context manager...\n")

    # Use async context manager - automatically starts and stops client
    async with CopilotPrompt() as prompt:
        print("Client started automatically!")

        # Send a prompt
        print("\nSending prompt: 'What are the benefits of Python?'")
        response = await prompt.send_prompt("What are the benefits of Python?")
        print(f"\nResponse: {response}")

        # Send another prompt
        print("\nSending prompt: 'What is async/await in Python?'")
        response = await prompt.send_prompt("What is async/await in Python?")
        print(f"\nResponse: {response}")

    # Client is automatically stopped here
    print("\nClient stopped automatically!")


if __name__ == "__main__":
    asyncio.run(main())
