"""
copilot_prompt.py - A convenient interface for making requests to GitHub Copilot.

This module provides the CopilotPrompt class which wraps the GitHub Copilot SDK
for easier prompting and interaction with Copilot.
"""

import asyncio
from typing import Optional, Dict
from copilot import CopilotClient


class CopilotPrompt:
    """
    A wrapper class for GitHub Copilot SDK that provides a convenient interface
    for making prompts to Copilot.

    This class handles client initialization, session management, and provides
    both streaming and non-streaming prompt methods.

    Authentication:
        The class relies on the GitHub Copilot CLI for authentication.
        Before using this class, ensure you have:
        1. Installed GitHub Copilot CLI
        2. Authenticated via: copilot auth login

        Optional environment variables:
        - COPILOT_CLI_PATH: Path to copilot CLI if not in system PATH

    Example:
        Basic usage with non-streaming response:

        >>> import asyncio
        >>> from copilotsdkv2 import CopilotPrompt
        >>>
        >>> async def main():
        ...     prompt = CopilotPrompt()
        ...     await prompt.start()
        ...     response = await prompt.send_prompt("What is 2+2?")
        ...     print(response)
        ...     await prompt.stop()
        >>>
        >>> asyncio.run(main())

        Using streaming responses:

        >>> async def main():
        ...     prompt = CopilotPrompt()
        ...     await prompt.start()
        ...
        ...     async for chunk in prompt.send_prompt_stream("Explain Python"):
        ...         print(chunk, end='', flush=True)
        ...
        ...     await prompt.stop()
        >>>
        >>> asyncio.run(main())

        Using as a context manager:

        >>> async def main():
        ...     async with CopilotPrompt() as prompt:
        ...         response = await prompt.send_prompt("Hello, Copilot!")
        ...         print(response)
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        cli_path: Optional[str] = None,
        model: str = "gpt-5",
        env: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the CopilotPrompt wrapper.

        Args:
            cli_path: Optional path to the Copilot CLI executable.
                     If not provided, assumes CLI is in system PATH.
            model: The model to use for prompts. Default is "gpt-5".
            env: Optional dictionary of environment variables to pass to the client.

        Note:
            The client is not started automatically. Call start() or use as
            async context manager to initialize the connection.
        """
        self.cli_path = cli_path
        self.model = model
        self.env = env
        self._client: Optional[CopilotClient] = None
        self._session = None
        self._started = False

    async def start(self) -> None:
        """
        Start the Copilot client and establish connection.

        This method must be called before sending any prompts.
        Alternatively, use the class as an async context manager.

        Raises:
            Exception: If client fails to start or connect.
        """
        if self._started:
            return

        client_kwargs = {}
        if self.cli_path:
            client_kwargs['cli_path'] = self.cli_path
        if self.env:
            client_kwargs['env'] = self.env

        self._client = CopilotClient(**client_kwargs)
        await self._client.start()
        self._started = True

    async def stop(self) -> None:
        """
        Stop the Copilot client and clean up resources.

        This method should be called when done using the client.
        If used as async context manager, this is called automatically.
        """
        if not self._started:
            return

        if self._session:
            try:
                await self._session.destroy()
            except Exception:
                pass
            self._session = None

        if self._client:
            try:
                await self._client.stop()
            except Exception:
                pass
            self._client = None

        self._started = False

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()
        return False

    async def _ensure_session(self) -> None:
        """
        Ensure a session exists and create one if needed.

        Raises:
            RuntimeError: If client has not been started.
        """
        if not self._started or not self._client:
            raise RuntimeError(
                "Client not started. Call start() or use as async context manager."
            )

        if not self._session:
            self._session = await self._client.create_session({"model": self.model})

    async def send_prompt(
        self,
        prompt: str,
        timeout: Optional[float] = 600.0
    ) -> str:
        """
        Send a prompt to Copilot and return the complete response.

        This method sends a prompt and waits for the complete response.
        For streaming responses, use send_prompt_stream() instead.

        Args:
            prompt: The prompt text to send to Copilot.
            timeout: Maximum time to wait for response in seconds.
                    Default is 30 seconds. None for no timeout.

        Returns:
            The complete response text from Copilot.

        Raises:
            RuntimeError: If client has not been started.
            asyncio.TimeoutError: If response takes longer than timeout.

        Example:
            >>> response = await prompt.send_prompt("What is Python?")
            >>> print(response)
        """
        await self._ensure_session()

        response_text = []
        done_event = asyncio.Event()
        error_container = []
        handler_lock = asyncio.Lock()

        def on_event(event):
            """Handle events from the session."""
            async def process_event():
                async with handler_lock:
                    try:
                        if event.type.value == "assistant.message":
                            if hasattr(event.data, 'content') and event.data.content:
                                response_text.append(event.data.content)
                        elif event.type.value == "session.idle":
                            done_event.set()
                        elif event.type.value == "error":
                            error_container.append(event.data)
                            done_event.set()
                    except Exception as e:
                        error_container.append(e)
                        done_event.set()

            # Schedule the async handler in the event loop
            asyncio.create_task(process_event())

        self._session.on(on_event)

        try:
            await self._session.send({"prompt": prompt})

            if timeout:
                await asyncio.wait_for(done_event.wait(), timeout=timeout)
            else:
                await done_event.wait()

            if error_container:
                raise Exception(f"Error during prompt: {error_container[0]}")

            return ''.join(response_text)

        finally:
            # Remove event handler
            try:
                self._session.off(on_event)
            except Exception:
                pass

    async def send_prompt_stream(
        self,
        prompt: str,
        timeout: Optional[float] = None
    ):
        """
        Send a prompt to Copilot and stream the response as it arrives.

        This method is an async generator that yields response chunks
        as they are received from Copilot.

        Args:
            prompt: The prompt text to send to Copilot.
            timeout: Optional maximum time to wait for response in seconds.

        Yields:
            str: Chunks of the response text as they arrive.

        Raises:
            RuntimeError: If client has not been started.
            asyncio.TimeoutError: If response takes longer than timeout.

        Example:
            >>> async for chunk in prompt.send_prompt_stream("Explain AI"):
            ...     print(chunk, end='', flush=True)
        """
        await self._ensure_session()

        chunk_queue = asyncio.Queue()
        done_event = asyncio.Event()
        error_container = []
        handler_lock = asyncio.Lock()

        def on_event(event):
            """Handle events from the session."""
            async def process_event():
                async with handler_lock:
                    try:
                        if event.type.value == "assistant.message":
                            if hasattr(event.data, 'content') and event.data.content:
                                await chunk_queue.put(event.data.content)
                        elif event.type.value == "session.idle":
                            await chunk_queue.put(None)
                            done_event.set()
                        elif event.type.value == "error":
                            error_container.append(event.data)
                            await chunk_queue.put(None)
                            done_event.set()
                    except Exception as e:
                        error_container.append(e)
                        await chunk_queue.put(None)
                        done_event.set()

            # Schedule the async handler in the event loop
            asyncio.create_task(process_event())

        self._session.on(on_event)

        try:
            await self._session.send({"prompt": prompt})

            # Yield chunks as they arrive
            while True:
                if timeout:
                    chunk = await asyncio.wait_for(chunk_queue.get(), timeout=timeout)
                else:
                    chunk = await chunk_queue.get()

                if chunk is None:
                    break

                yield chunk

            if error_container:
                raise Exception(f"Error during streaming prompt: {error_container[0]}")

        finally:
            # Remove event handler
            try:
                self._session.off(on_event)
            except Exception:
                pass

    async def configure(
        self,
        model: Optional[str] = None,
        cli_path: Optional[str] = None
    ) -> None:
        """
        Update configuration options.

        This method allows updating configuration after initialization.
        Note: Changes to cli_path require restart() to take effect.

        Args:
            model: New model to use for prompts.
            cli_path: New path to Copilot CLI.

        Example:
            >>> await prompt.configure(model="gpt-4")
        """
        if model:
            self.model = model
            # If session exists, recreate it with new model
            if self._session:
                await self._session.destroy()
                self._session = await self._client.create_session({"model": self.model})

        if cli_path:
            self.cli_path = cli_path
            # Note: CLI path change requires client restart

    async def restart(self) -> None:
        """
        Restart the client connection.

        Useful after configuration changes that require reconnection.

        Example:
            >>> await prompt.configure(cli_path="/new/path/to/cli")
            >>> await prompt.restart()
        """
        await self.stop()
        await self.start()
