from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('commit')
class Commit(BaseCommand):
    """Git commit command realisation"""
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.message = parameters.get("message")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "commit", "-m", self.message], self.cwd)
