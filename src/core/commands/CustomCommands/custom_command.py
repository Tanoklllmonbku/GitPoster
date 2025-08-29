from src.core.commands.AbsClass import BaseCommand, CommandFormat
from src.core.commands import CommandFactory


class CustomCommandInterface(BaseCommand):
    name = "Unnamed"
    command_format: CommandFormat = None

    def __init__(self, cmd):
        super().__init__()