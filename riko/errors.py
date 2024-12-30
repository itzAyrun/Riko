from discord.ext.commands import CheckFailure


class NotDeveloper(CheckFailure):
    def __init__(self, message="This is a developer-only command!"):
        super().__init__(message)
