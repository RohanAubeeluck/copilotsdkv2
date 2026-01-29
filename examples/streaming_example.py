"""
Streaming response example for CopilotPrompt.

This example demonstrates how to use streaming responses to get
chunks of the response as they arrive from Copilot.
"""

import asyncio
from copilotsdkv2 import CopilotPrompt


async def main():
    """Main function demonstrating streaming responses."""
    print("Demonstrating streaming responses...\n")

    async with CopilotPrompt() as prompt:
        # Example 1: Stream a haiku
        print("Prompt: 'Write a haiku about coding'\n")
        print("Response (streaming): ", end='', flush=True)
        async for chunk in prompt.send_prompt_stream("Write a haiku about coding"):
            print(chunk, end='', flush=True)
        print("\n")

        # Example 2: Stream a longer response
        print("\nPrompt: 'Explain the benefits of async programming'\n")
        print("Response (streaming): ", end='', flush=True)
        async for chunk in prompt.send_prompt_stream(
            "Explain the benefits of async programming in 2-3 sentences"
        ):
            print(chunk, end='', flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
