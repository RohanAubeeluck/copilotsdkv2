"""
Configuration example for CopilotPrompt.

This example demonstrates various configuration options including
custom model selection and runtime configuration updates.
"""

import asyncio
from copilotsdkv2 import CopilotPrompt


async def main():
    """Main function demonstrating configuration options."""
    print("Demonstrating CopilotPrompt configuration...\n")

    # Example 1: Initialize with custom model
    print("Example 1: Using custom model configuration")
    async with CopilotPrompt(model="gpt-4") as prompt:
        print(f"Current model: {prompt.model}")
        response = await prompt.send_prompt("What is Python?")
        print(f"Response: {response}\n")

    # Example 2: Change model at runtime
    print("\nExample 2: Changing model at runtime")
    async with CopilotPrompt() as prompt:
        print(f"Initial model: {prompt.model}")
        response1 = await prompt.send_prompt("Count to 3")
        print(f"Response 1: {response1}")

        # Update configuration
        print("\nUpdating to gpt-4...")
        await prompt.configure(model="gpt-4")
        print(f"New model: {prompt.model}")

        response2 = await prompt.send_prompt("Count to 3 again")
        print(f"Response 2: {response2}\n")

    # Example 3: Custom CLI path (if needed)
    print("\nExample 3: Custom CLI path configuration")
    # Uncomment and modify if you need a custom CLI path
    # async with CopilotPrompt(cli_path="/custom/path/to/copilot") as prompt:
    #     response = await prompt.send_prompt("Hello!")
    #     print(f"Response: {response}")
    print("(Skipped - use default CLI path)\n")

    print("Configuration examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
