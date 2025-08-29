from typing import NamedTuple, Any


class CommandFormat(NamedTuple):
    """Data format for git commands"""
    command: list[str]
    cwd: Any