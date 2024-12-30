from discord.ext import commands
from discord.ext.commands import Context, NotOwner

from riko.errors import NotDeveloper
from config import settings


def developer_only():
    def predicate(ctx: Context):
        settings.reload()
        if ctx.author.id in settings["id.developers"]:
            return True
        raise NotDeveloper()

    return commands.check(predicate)


def owner_only():
    def predicate(ctx: Context):
        settings.reload()
        if ctx.author.id in settings["id.owners"]:
            return True
        raise NotOwner("This is an owner-only command!")

    return commands.check(predicate)
