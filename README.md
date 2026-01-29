# GitHub Copilot SDK v2

A Python SDK and demo application for interacting with GitHub Copilot Chat API.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/RohanAubeeluck/copilotsdkv2.git
cd copilotsdkv2
pip install -r requirements.txt

# Set your GitHub token
export GITHUB_TOKEN="your_github_oauth_token_here"

# Run the demo app
python app.py "Explain what Python decorators are"
```

## Features

- 🤖 Send prompts to GitHub Copilot Chat and receive AI-powered responses
- 🔐 Secure token handling with environment variable support
- 🎯 Simple command-line interface
- 📦 Minimal dependencies (only `requests` required)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/RohanAubeeluck/copilotsdkv2.git
cd copilotsdkv2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

You need a GitHub OAuth token to use this application. There are three ways to configure it:

### Option 1: Environment Variable (Recommended)

Set the `GITHUB_TOKEN` environment variable:

```bash
export GITHUB_TOKEN="your_github_oauth_token_here"
```

### Option 2: Update the Code

Edit `copilot_sdk/auth.py` and replace the placeholder:

```python
GITHUB_TOKEN = "your_github_oauth_token_here"  # Replace "REPLACE_ME"
```

### Option 3: Pass Programmatically

When using the SDK in your own code:

```python
from copilot_sdk import CopilotClient

client = CopilotClient(github_token="your_token_here")
```

### Getting a GitHub Token

To obtain a GitHub OAuth token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token (classic)
3. You need a token with Copilot access (requires an active GitHub Copilot subscription)

**Note:** Never commit real tokens to version control!

## Usage

### Command Line

Run the demo application with a prompt:

```bash
python app.py "Explain what async/await does in Python"
```

Or with a longer prompt:

```bash
python app.py "Write a Python function that calculates the factorial of a number"
```

### As a Library

You can also use the SDK in your own Python code:

```python
from copilot_sdk import CopilotClient

# Create client
client = CopilotClient()

# Send a prompt
response = client.send_chat_message("What is the meaning of life?")

# Get the response text
text = client.get_completion_text(response)
print(text)
```

## Project Structure

```
copilotsdkv2/
├── app.py                  # Main demo application
├── copilot_sdk/            # SDK package
│   ├── __init__.py         # Package initialization
│   ├── auth.py             # Authentication and token handling
│   └── client.py           # Copilot API client
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## How It Works

1. **Authentication**: The SDK exchanges your GitHub OAuth token for a Copilot-specific bearer token
2. **API Call**: Sends your prompt to the GitHub Copilot Chat API endpoint
3. **Response**: Receives and displays the AI-generated response

The SDK handles all the API communication, headers, and token management automatically.

## Example Output

```bash
$ python app.py "What is a list comprehension in Python?"

Sending prompt to GitHub Copilot Chat: What is a list comprehension in Python?
------------------------------------------------------------
Response from GitHub Copilot:
------------------------------------------------------------
A list comprehension is a concise way to create lists in Python. It consists
of brackets containing an expression followed by a for clause, then zero or
more for or if clauses. The result will be a new list resulting from evaluating
the expression in the context of the for and if clauses.

Example:
squares = [x**2 for x in range(10)]
# Result: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
------------------------------------------------------------
```

## Security Notes

- ⚠️ The placeholder token `REPLACE_ME` in `auth.py` is intentionally invalid
- ✅ Always use environment variables for sensitive tokens
- 🔒 Never commit real tokens to version control
- 🛡️ The `.gitignore` file excludes `.env` files to prevent accidental commits

## API Endpoints

This SDK uses the following GitHub Copilot API endpoints:

- **Token Exchange**: `https://api.github.com/copilot_internal/v2/token`
- **Chat Completions**: `https://api.githubcopilot.com/chat/completions`

**⚠️ Important Note About API Stability:**

The token exchange endpoint uses an internal GitHub API (`copilot_internal/v2/token`) that is not officially documented. This means:
- The API may change without notice
- It may stop working if GitHub modifies their internal infrastructure
- This SDK is intended for demonstration and educational purposes
- For production use, consider using official GitHub APIs when they become available

## Requirements

- Python 3.7+
- `requests` library (2.31.0+)
- Active GitHub Copilot subscription
- Valid GitHub OAuth token with Copilot access

## Troubleshooting

### "GitHub token not configured" error

Make sure you've set the `GITHUB_TOKEN` environment variable or updated the constant in `auth.py`.

### "Failed to get Copilot token" error

- Verify your GitHub token is valid
- Ensure you have an active GitHub Copilot subscription
- Check your internet connection

### "Failed to send chat message" error

- The Copilot token may have expired (tokens are short-lived)
- Try running the app again to get a fresh token
- Check that the API endpoints are accessible

## License

This project is provided as-is for demonstration purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.