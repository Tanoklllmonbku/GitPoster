from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('log')
class Log(BaseCommand):
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.cmd = parameters.get("cmd")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "log"] + self.cmd, self.cwd)


