# commands/remote.py
# def git_remote_add_origin(url: str, cwd):
#     return ["git", "remote", "add", "origin", url], cwd


from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('remote_add_origin')
class RemoteAddOrigin(BaseCommand):
    def __init__(self, parameters):
        super().__init__()
        self.url = parameters.get('url')
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "remote", "add", "origin", self.url], self.cwd)