# commands/add.py
# def git_add_files(files, cwd):
#     return ["git", "add"] + files, cwd


from src.core.commands.AbsClass import BaseCommand
from AbsClass import CommandFormat
from src.core.commands import CommandFactory

@CommandFactory.reg('add')
class Add(BaseCommand):
    def __init__(self, parameters):
        super().__init__()
        self.files = parameters.get("files")
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "add"] + self.files, self.cwd)
