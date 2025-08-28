# commands/status.py
# def git_status_porcelain(cwd):
#     return ["git", "status", "--porcelain", "-u"], cwd


from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('status')
class Status(BaseCommand):
    def __init__(self, parameters):
        super().__init__()
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "status", "--porcelain", "-u"], self.cwd)