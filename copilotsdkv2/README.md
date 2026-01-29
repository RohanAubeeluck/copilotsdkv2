# copilotsdkv2 wrapper

This folder contains a small convenience wrapper (`CopilotPrompt`) around the `github-copilot-sdk` package, plus a tiny CLI so you can send prompts from the terminal.

## Prereqs

- Python installed
- Dependencies installed (from the repo root):

```powershell
pip install -r requirements.txt
```

- You must be authenticated the way `github-copilot-sdk` expects (often via the GitHub Copilot CLI login flow). If you're using the Copilot CLI, run:

```powershell
copilot auth login
```

## CLI usage

From the repo root:

```powershell
python -m copilotsdkv2 "Explain async/await in Python"
```

Streaming output:

```powershell
python -m copilotsdkv2 --stream "Write a Python function to reverse a list"
```

Choose a model:

```powershell
python -m copilotsdkv2 --model gpt-5 "Give me 5 examples of list comprehensions"
```

## Library usage

```python
import asyncio
from copilotsdkv2 import CopilotPrompt

async def main():
    async with CopilotPrompt(model="gpt-5") as prompt:
        resp = await prompt.send_prompt("What is 2+2?")
        print(resp)

asyncio.run(main())
```
