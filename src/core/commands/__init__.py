from src.core.commands.AbsClass import BaseCommand, CommandFormat
from src.core.commands.CustomCommands import CustomCommand


class CommandFactory:
    """Factory for creating needed commands."""
    _reg = {}

    @classmethod
    def reg(cls, name: str):
        def decorator(command_class):
            if not issubclass(command_class, BaseCommand):
                raise TypeError("Command class is not subclass of BaseCommand")
            cls._reg[name] = command_class
            return command_class
        return decorator

    @classmethod
    def reg_from_cfg(cls, config: dict):
        name: str = config.get("name")
        command_format: CommandFormat = config.get("command_format")
        NewCommand = type(
            f"Custom{name}",
            (CustomCommand,),
            {"name": name, "command_format": command_format},
        )
        cls.reg(name)(NewCommand)

    def __init__(self, command_name):
        self.command_name = command_name # Name of command (For calling)

    def __call__(self, parameters):
        if not self.command_name in self._reg:
            raise ValueError("Command '{}' is not registered".format(self.command_name))
        return self._reg[self.command_name](parameters)


def reg_custom_command(config: dict):
    if not isinstance(config, dict):
        raise ValueError("config is not a dict")
    CommandFactory.reg_from_cfg(config)

    return CommandFactory(config.get("name"))

def return_base_command(name:str, parameters:dict):
    factory = CommandFactory(name)
    result = factory(parameters)
    return result().command, result().cwd


