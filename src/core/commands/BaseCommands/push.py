# commands/push.py
# def git_push(cwd):
#     return ["git", "push"], cwd

from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('push')
class Push(BaseCommand):
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "push"], self.cwd)