# Examples

This directory contains example scripts demonstrating how to use the GitHub Copilot SDK.

## Available Examples

### simple_usage.py
A minimal example showing basic SDK usage:
```bash
python examples/simple_usage.py
```

### advanced_usage.py
An advanced example demonstrating:
- Processing multiple prompts
- Error handling
- Response formatting

```bash
python examples/advanced_usage.py
```

## Running the Examples

All examples require a GitHub token. Set it as an environment variable:

```bash
export GITHUB_TOKEN="your_github_token_here"
python examples/simple_usage.py
```

Or update the `GITHUB_TOKEN` constant in `copilot_sdk/auth.py`.
