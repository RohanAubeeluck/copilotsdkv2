"""
Tests for CopilotPrompt class.

These tests verify the functionality of the CopilotPrompt wrapper class.
Note: These tests use mocking to avoid requiring actual Copilot authentication.
"""

import asyncio
import pytest
from unittest.mock import Mock, AsyncMock, patch
from copilotsdkv2 import CopilotPrompt


@pytest.fixture
def mock_copilot_client():
    """Create a mock CopilotClient for testing."""
    with patch('copilotsdkv2.copilot_prompt.CopilotClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        # Mock session
        mock_session = AsyncMock()
        mock_client.create_session = AsyncMock(return_value=mock_session)

        yield mock_client_class, mock_client, mock_session


class TestCopilotPromptInit:
    """Test initialization of CopilotPrompt."""

    def test_init_default(self):
        """Test initialization with default parameters."""
        prompt = CopilotPrompt()
        assert prompt.model == "gpt-5"
        assert prompt.cli_path is None
        assert prompt.env is None
        assert prompt._client is None
        assert prompt._session is None
        assert prompt._started is False

    def test_init_with_params(self):
        """Test initialization with custom parameters."""
        prompt = CopilotPrompt(
            cli_path="/custom/path",
            model="gpt-4",
            env={"KEY": "value"}
        )
        assert prompt.model == "gpt-4"
        assert prompt.cli_path == "/custom/path"
        assert prompt.env == {"KEY": "value"}


class TestCopilotPromptLifecycle:
    """Test lifecycle methods (start, stop, context manager)."""

    @pytest.mark.asyncio
    async def test_start(self, mock_copilot_client):
        """Test starting the client."""
        mock_client_class, mock_client, _ = mock_copilot_client

        prompt = CopilotPrompt()
        await prompt.start()

        assert prompt._started is True
        mock_client.start.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_with_cli_path(self, mock_copilot_client):
        """Test starting with custom CLI path."""
        mock_client_class, mock_client, _ = mock_copilot_client

        prompt = CopilotPrompt(cli_path="/custom/path", env={"KEY": "val"})
        await prompt.start()

        mock_client_class.assert_called_once_with(
            cli_path="/custom/path",
            env={"KEY": "val"}
        )

    @pytest.mark.asyncio
    async def test_start_idempotent(self, mock_copilot_client):
        """Test that calling start multiple times is safe."""
        _, mock_client, _ = mock_copilot_client

        prompt = CopilotPrompt()
        await prompt.start()
        await prompt.start()

        # Should only start once
        assert mock_client.start.call_count == 1

    @pytest.mark.asyncio
    async def test_stop(self, mock_copilot_client):
        """Test stopping the client."""
        _, mock_client, mock_session = mock_copilot_client

        prompt = CopilotPrompt()
        await prompt.start()
        prompt._session = mock_session
        await prompt.stop()

        assert prompt._started is False
        assert prompt._client is None
        assert prompt._session is None
        mock_session.destroy.assert_called_once()
        mock_client.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_without_start(self, mock_copilot_client):
        """Test stopping without starting is safe."""
        prompt = CopilotPrompt()
        await prompt.stop()
        assert prompt._started is False

    @pytest.mark.asyncio
    async def test_context_manager(self, mock_copilot_client):
        """Test using as async context manager."""
        _, mock_client, _ = mock_copilot_client

        async with CopilotPrompt() as prompt:
            assert prompt._started is True
            mock_client.start.assert_called_once()

        # Should auto-stop on exit
        mock_client.stop.assert_called_once()


class TestCopilotPromptPrompting:
    """Test prompt sending functionality."""

    @pytest.mark.asyncio
    async def test_send_prompt_not_started(self):
        """Test that send_prompt raises error if not started."""
        prompt = CopilotPrompt()

        with pytest.raises(RuntimeError, match="Client not started"):
            await prompt.send_prompt("test")

    @pytest.mark.asyncio
    async def test_send_prompt_success(self, mock_copilot_client):
        """Test successful prompt sending."""
        _, mock_client, mock_session = mock_copilot_client

        # Setup mock event handler
        captured_handler = None

        def capture_on(handler):
            nonlocal captured_handler
            captured_handler = handler

        mock_session.on = Mock(side_effect=capture_on)
        mock_session.off = Mock()
        mock_session.send = AsyncMock()

        prompt = CopilotPrompt()
        await prompt.start()

        # Simulate sending prompt and receiving response
        async def simulate_response():
            await asyncio.sleep(0.01)
            if captured_handler:
                # Simulate assistant message
                event = Mock()
                event.type.value = "assistant.message"
                event.data.content = "Test response"
                captured_handler(event)

                # Simulate session idle
                event2 = Mock()
                event2.type.value = "session.idle"
                captured_handler(event2)

        asyncio.create_task(simulate_response())

        response = await prompt.send_prompt("What is 2+2?", timeout=5.0)

        assert response == "Test response"
        mock_session.send.assert_called_once_with({"prompt": "What is 2+2?"})

    @pytest.mark.asyncio
    async def test_send_prompt_timeout(self, mock_copilot_client):
        """Test prompt timeout."""
        _, mock_client, mock_session = mock_copilot_client

        mock_session.on = Mock()
        mock_session.off = Mock()
        mock_session.send = AsyncMock()

        prompt = CopilotPrompt()
        await prompt.start()

        # Should timeout because no response
        with pytest.raises(asyncio.TimeoutError):
            await prompt.send_prompt("test", timeout=0.1)

    @pytest.mark.asyncio
    async def test_send_prompt_stream(self, mock_copilot_client):
        """Test streaming prompt response."""
        _, mock_client, mock_session = mock_copilot_client

        captured_handler = None

        def capture_on(handler):
            nonlocal captured_handler
            captured_handler = handler

        mock_session.on = Mock(side_effect=capture_on)
        mock_session.off = Mock()
        mock_session.send = AsyncMock()

        prompt = CopilotPrompt()
        await prompt.start()

        # Simulate streaming response
        async def simulate_stream():
            await asyncio.sleep(0.01)
            if captured_handler:
                # Send multiple chunks
                for chunk in ["Hello", " ", "World"]:
                    event = Mock()
                    event.type.value = "assistant.message"
                    event.data.content = chunk
                    captured_handler(event)
                    await asyncio.sleep(0.01)

                # Signal completion
                event = Mock()
                event.type.value = "session.idle"
                captured_handler(event)

        asyncio.create_task(simulate_stream())

        chunks = []
        async for chunk in prompt.send_prompt_stream("test", timeout=5.0):
            chunks.append(chunk)

        assert chunks == ["Hello", " ", "World"]
        mock_session.send.assert_called_once_with({"prompt": "test"})


class TestCopilotPromptConfiguration:
    """Test configuration methods."""

    @pytest.mark.asyncio
    async def test_configure_model(self, mock_copilot_client):
        """Test updating model configuration."""
        _, mock_client, mock_session = mock_copilot_client

        prompt = CopilotPrompt()
        await prompt.start()

        # Create a session first by calling _ensure_session
        await prompt._ensure_session()
        assert mock_client.create_session.call_count == 1

        await prompt.configure(model="gpt-4")

        assert prompt.model == "gpt-4"
        # Should recreate session with new model
        mock_session.destroy.assert_called_once()
        assert mock_client.create_session.call_count == 2

    @pytest.mark.asyncio
    async def test_configure_cli_path(self, mock_copilot_client):
        """Test updating CLI path."""
        prompt = CopilotPrompt()

        await prompt.configure(cli_path="/new/path")

        assert prompt.cli_path == "/new/path"

    @pytest.mark.asyncio
    async def test_restart(self, mock_copilot_client):
        """Test restarting the client."""
        _, mock_client, _ = mock_copilot_client

        prompt = CopilotPrompt()
        await prompt.start()
        await prompt.restart()

        assert mock_client.stop.call_count == 1
        assert mock_client.start.call_count == 2
