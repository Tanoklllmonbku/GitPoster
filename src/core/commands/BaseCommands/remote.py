from src.core.commands.AbsClass import CommandFormat, BaseCommand
from src.core.commands import CommandFactory


@CommandFactory.reg('remote_add_origin')
class RemoteAddOrigin(BaseCommand):
    """Remote repository initialization command."""
    def __init__(self, parameters:dict):
        super().__init__(parameters)
        self.url = parameters.get('url')
        self.cwd = parameters.get("cwd")

    def execute(self) -> CommandFormat:
        return CommandFormat(["git", "remote", "add", "origin", self.url], self.cwd)