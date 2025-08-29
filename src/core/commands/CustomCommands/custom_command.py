from src.core.commands import BaseCommand, CommandFormat

class CustomCommand(BaseCommand):
    name:str = "Unnamed"
    command_format: CommandFormat

    def __init__(self, parameters):
        super().__init__(parameters)

    def execute(self):
        if not self.command_format:
            raise TypeError("No command format")

        return self.command_format
