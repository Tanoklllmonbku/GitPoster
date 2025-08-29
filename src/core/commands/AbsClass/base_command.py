from abc import ABC, abstractmethod
from .command_format import CommandFormat


class BaseCommand(ABC):
    """Parent class for creating git commands"""
    def __init__(self, parameters):
        self.parameters = parameters

    def __call__(self) -> CommandFormat:
        return self.execute()

    @abstractmethod
    def execute(self) -> CommandFormat:
        pass # Executing logic (In children)
