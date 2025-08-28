# commands/init.py
# def git_init(cwd):
#     return ["git", "init"], cwd

from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('init')
class Init(BaseCommand):
    def __init__(self, parameters):
        super().__init__()
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "init"], self.cwd)