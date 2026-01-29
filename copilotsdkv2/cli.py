"""CLI for the CopilotPrompt wrapper.

This is a lightweight command-line interface so you can run:

  python -m copilotsdkv2.cli "your prompt"

It relies on the `github-copilot-sdk` package, which typically authenticates
via the GitHub Copilot CLI login flow (per the SDK's own docs).
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from .copilot_prompt import CopilotPrompt


async def _run(prompt: str, model: str, stream: bool) -> int:
    async with CopilotPrompt(model=model) as cp:
        if stream:
            async for chunk in cp.send_prompt_stream(prompt):
                # Print chunks as they arrive.
                print(chunk, end="", flush=True)
            print()  # newline
        else:
            text = await cp.send_prompt(prompt)
            print(text)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Send a prompt using CopilotPrompt")
    parser.add_argument("prompt", nargs="+", help="Prompt text")
    parser.add_argument("--model", default="gpt-5", help="Model name (default: gpt-5)")
    parser.add_argument("--stream", action="store_true", help="Stream output as it arrives")

    args = parser.parse_args(argv)
    prompt = " ".join(args.prompt)

    try:
        return asyncio.run(_run(prompt, model=args.model, stream=args.stream))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
