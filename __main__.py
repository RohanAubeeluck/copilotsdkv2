"""Entrypoint for `python -m copilotsdkv2`.

Delegates to the CLI.
"""

from .prompt import main


if __name__ == "__main__":
    raise SystemExit(main())
