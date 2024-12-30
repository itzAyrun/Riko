from datetime import datetime
from typing import List
import os
import logging

from discord import Embed, Intents, Message
from discord.ext.commands import (
    Bot,
    BotMissingPermissions,
    CommandError,
    CommandNotFound,
    CommandOnCooldown,
    Context,
    MissingRequiredArgument,
    NotOwner,
)
from discord.ext import commands

from riko.errors import NotDeveloper
from riko.emojis import PINK_ERROR
from config import settings

logger = logging.getLogger()


class Riko(Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=self._get_prefix,
            intents=Intents.all(),
            help_command=None,
            strip_after_prefix=settings["commands.strip_after_prefix"],
            case_insensitive=settings["commands.case_insensitive"],
        )

    @staticmethod
    async def _get_prefix(bot: "Riko", message: Message) -> List[str]:
        settings.reload()

        # Since the commands.when_mentioned_or function takes in a list of prefixes
        # We need to grab the prefix and store it as a list
        prefix: List[str] = [settings["commands.prefix"]]

        return commands.when_mentioned_or(*prefix)(bot, message)

    @staticmethod
    def error_embed(message: str) -> Embed:
        return Embed(description=f"{PINK_ERROR} {message}", timestamp=datetime.now())

    async def _load_cogs(self) -> None:
        for f in os.listdir("riko/cogs"):
            if f in ["__pycache__", "__init__.py"] or not f.endswith(".py"):
                continue  # ignore

            else:
                await self.load_extension(f"riko.cogs.{f[:-3]}")
                logger.info(f"Loaded {f}")

    async def setup_hook(self) -> None:
        await self._load_cogs()

    async def on_ready(self) -> None:
        logger.info(f"Logged in as {self.user}")

    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        if hasattr(ctx, "_local_handler"):
            return

        if isinstance(error, CommandNotFound):
            return

        if isinstance(error, CommandOnCooldown):
            await ctx.reply(
                embed=self.error_embed(
                    f"Patience, darling. Even I need a moment to catch my breath. Try again in `{error.retry_after:.2f}` seconds."
                )
            )

        elif isinstance(error, BotMissingPermissions):
            missing_perms = "\n".join(error.missing_permissions)
            await ctx.reply(
                embed=self.error_embed(
                    f"Tsk I can't work my magic without the proper power. Grant me the permissions I need, or I simply won't play along\n\n`{missing_perms}`"
                )
            )

        elif isinstance(error, MissingRequiredArgument):
            if ctx.command is not None:
                settings.reload()
                prefix: str = settings["commands.prefix"]
                await ctx.reply(
                    embed=self.error_embed(
                        f"Tsk, darling! You're missing something important. Here's how to do it properly:\n\n`{prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
                    )
                )

        elif isinstance(error, NotOwner):
            await ctx.reply(
                embed=self.error_embed(
                    "You're not the rightful owner, darling. Only the chosen one may command me."
                )
            )

        elif isinstance(error, NotDeveloper):
            await ctx.reply(
                embed=self.error_embed(
                    "This is a developer-only command! Contact the developer/maintainer for more info."
                )
            )

        else:
            logger.error(str(error), exc_info=error)
