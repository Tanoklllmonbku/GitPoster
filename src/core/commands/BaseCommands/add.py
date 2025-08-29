from src.core.commands.AbsClass import BaseCommand, CommandFormat
from src.core.commands import CommandFactory


@CommandFactory.reg('add')
class Add(BaseCommand):
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.files = parameters.get("files")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "add"] + self.files, self.cwd)
