from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('log')
class Commit(BaseCommand):
    def __init__(self, parameters):
        super().__init__()
        self.cmd = parameters.get("cmd")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "log", self.cmd], self.cwd)