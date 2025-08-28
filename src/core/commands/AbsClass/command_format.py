from typing import NamedTuple, Any


class CommandFormat(NamedTuple):
    command: list[str]
    cwd: Any