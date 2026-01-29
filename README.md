# copilotsdkv2

A convenient Python interface for making requests to GitHub Copilot using the `github-copilot-sdk`.

## Features

- **Easy-to-use wrapper** around the GitHub Copilot SDK
- **Multiple response modes**: Standard and streaming responses
- **Async/await support** with context manager pattern
- **Configurable authentication** with environment variable support
- **Comprehensive error handling** and timeouts
- **Full type hints** and documentation

## Installation

### Prerequisites

Before using this package, you need to:

1. Install the GitHub Copilot CLI (if not already installed)
2. Authenticate with GitHub Copilot:
   ```bash
   copilot auth login
   ```

### Install the package

```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start

### Basic Usage

```python
import asyncio
from copilotsdkv2 import CopilotPrompt

async def main():
    # Create a CopilotPrompt instance
    prompt = CopilotPrompt()

    # Start the client
    await prompt.start()

    # Send a prompt and get response
    response = await prompt.send_prompt("What is 2+2?")
    print(response)

    # Clean up
    await prompt.stop()

asyncio.run(main())
```

### Using Context Manager (Recommended)

```python
import asyncio
from copilotsdkv2 import CopilotPrompt

async def main():
    async with CopilotPrompt() as prompt:
        response = await prompt.send_prompt("Explain Python decorators")
        print(response)

asyncio.run(main())
```

### Streaming Responses

```python
import asyncio
from copilotsdkv2 import CopilotPrompt

async def main():
    async with CopilotPrompt() as prompt:
        print("Response: ", end='', flush=True)
        async for chunk in prompt.send_prompt_stream("Write a haiku about coding"):
            print(chunk, end='', flush=True)
        print()  # New line at end

asyncio.run(main())
```

### Custom Configuration

```python
import asyncio
from copilotsdkv2 import CopilotPrompt

async def main():
    # Initialize with custom settings
    prompt = CopilotPrompt(
        cli_path="/custom/path/to/copilot",  # Optional: custom CLI path
        model="gpt-4",                        # Optional: specify model
        env={"CUSTOM_VAR": "value"}          # Optional: environment variables
    )

    async with prompt:
        response = await prompt.send_prompt("Hello, Copilot!")
        print(response)

asyncio.run(main())
```

### Updating Configuration

```python
import asyncio
from copilotsdkv2 import CopilotPrompt

async def main():
    async with CopilotPrompt() as prompt:
        # Use default model
        response1 = await prompt.send_prompt("What is Python?")

        # Switch to a different model
        await prompt.configure(model="gpt-4")
        response2 = await prompt.send_prompt("What is Python?")

asyncio.run(main())
```

## Authentication

This package relies on the GitHub Copilot CLI for authentication. The CLI must be authenticated before using this package.

### Authentication Steps

1. Install GitHub Copilot CLI (if not already installed)
2. Run the authentication command:
   ```bash
   copilot auth login
   ```
3. Follow the browser-based authentication flow

### Environment Variables

- `COPILOT_CLI_PATH`: Optional. Specify a custom path to the Copilot CLI if it's not in your system PATH.

You can also pass environment variables directly when initializing:

```python
prompt = CopilotPrompt(env={"COPILOT_CLI_PATH": "/custom/path"})
```

## API Reference

### CopilotPrompt Class

#### `__init__(cli_path=None, model="gpt-5", env=None)`

Initialize the CopilotPrompt wrapper.

**Parameters:**
- `cli_path` (str, optional): Path to the Copilot CLI executable
- `model` (str, optional): Model to use for prompts (default: "gpt-5")
- `env` (dict, optional): Environment variables to pass to the client

#### `async start()`

Start the Copilot client and establish connection.

**Raises:**
- `Exception`: If client fails to start

#### `async stop()`

Stop the Copilot client and clean up resources.

#### `async send_prompt(prompt, timeout=30.0)`

Send a prompt to Copilot and return the complete response.

**Parameters:**
- `prompt` (str): The prompt text to send
- `timeout` (float, optional): Maximum time to wait in seconds (default: 30.0)

**Returns:**
- `str`: Complete response from Copilot

**Raises:**
- `RuntimeError`: If client has not been started
- `asyncio.TimeoutError`: If response takes longer than timeout

#### `async send_prompt_stream(prompt, timeout=None)`

Send a prompt to Copilot and stream the response.

**Parameters:**
- `prompt` (str): The prompt text to send
- `timeout` (float, optional): Maximum time to wait in seconds

**Yields:**
- `str`: Chunks of the response as they arrive

**Raises:**
- `RuntimeError`: If client has not been started
- `asyncio.TimeoutError`: If response takes longer than timeout

#### `async configure(model=None, cli_path=None)`

Update configuration options.

**Parameters:**
- `model` (str, optional): New model to use
- `cli_path` (str, optional): New CLI path (requires restart)

#### `async restart()`

Restart the client connection.

## Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=copilotsdkv2 tests/

# Run with verbose output
pytest -v tests/
```

## Examples

See the `examples/` directory for more usage examples:

- `basic_usage.py` - Simple prompt and response
- `streaming_example.py` - Streaming responses
- `context_manager_example.py` - Using context manager pattern
- `configuration_example.py` - Custom configuration

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/RohanAubeeluck/copilotsdkv2.git
cd copilotsdkv2

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

### Code Style

This project follows PEP 8 style guidelines. Make sure your code:
- Uses 4 spaces for indentation
- Has no trailing whitespace
- Includes docstrings for all public methods
- Uses type hints where appropriate

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/RohanAubeeluck/copilotsdkv2/issues)
- Check the [GitHub Copilot SDK documentation](https://github.com/github/copilot-sdk)

## Acknowledgments

This package is a wrapper around the [GitHub Copilot SDK](https://github.com/github/copilot-sdk).