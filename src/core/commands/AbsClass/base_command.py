from abc import ABC, abstractmethod
from .command_format import CommandFormat


class BaseCommand(ABC):
    """Interface for using git commands"""
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self) -> CommandFormat:
        return self.execute()

    @abstractmethod
    def execute(self) -> CommandFormat:
        pass # Executing logic (In children)

