from src.core.commands.AbsClass.base_command import BaseCommand


#__all__ = ["git_add_files", "git_commit", "git_init", "git_status_porcelain", "git_push"]


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

    def __init__(self, command_name):
        self.command_name = command_name # Name of command (For calling)

    def __call__(self, **kwargs):
        if not self.command_name in self._reg:
            raise ValueError("Command '{}' is not registered".format(self.command_name))
        return self._reg[self.command_name](**kwargs)
