# commands/commit.py
# def git_commit(message, cwd):
#     return ["git", "commit", "-m", message], cwd
from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('commit')
class Commit(BaseCommand):
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.message = parameters.get("message")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "commit", "-m", self.message], self.cwd)
