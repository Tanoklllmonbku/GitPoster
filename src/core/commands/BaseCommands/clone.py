from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('clone')
class Clone(BaseCommand):
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.url = parameters.get("url")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "clone", self.url], self.cwd)
