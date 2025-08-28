from src.core.commands.AbsClass import BaseCommand, CommandFormat
from src.core.commands import CommandFactory


@CommandFactory.reg("branch")
class Commit(BaseCommand):
    def __init__(self, parameters):
        super().__init__()
        self.message = parameters.get("message")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "commit", "-m", self.message], self.cwd)
