# commands/status.py
from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('status')
class Status(BaseCommand):
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "status", "--porcelain", "-u"], self.cwd)