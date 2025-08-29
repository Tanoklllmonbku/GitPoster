# commands/init.py
# def git_init(cwd):
#     return ["git", "init"], cwd

from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg("Init")
class Init(BaseCommand):
    """Git init command realisation"""
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "init"], self.cwd)