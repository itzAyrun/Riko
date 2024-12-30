from discord import Embed
from discord.ext import commands
from discord.ext.commands import BucketType, Cog, Context
import aiofiles
import toml

from config import settings
from riko import Riko
from riko.checks import owner_only
from riko.emojis import SETTINGS_INFO


class Prefix(Cog):
    def __init__(self, bot: Riko) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.cooldown(rate=1, per=5, type=BucketType.guild)
    @commands.guild_only()
    async def prefix(self, ctx: Context) -> None:
        await self.list(ctx)

    @prefix.command(aliases=["display", "show", "get"])
    async def list(self, ctx: Context) -> None:
        settings.reload()
        await ctx.reply(
            embed=Embed(
                description=f"{SETTINGS_INFO} The current prefix for this server is: `{settings['commands.prefix']}`"
            )
        )

    @prefix.command(aliases=["update", "change"])
    @owner_only()
    async def set(self, ctx: Context, new_prefix: str) -> None:
        if len(new_prefix) > 2:
            await ctx.reply(
                embed=self.bot.error_embed(
                    "Darling, keep it simple. A prefix longer than 2 characters? Stick to the rules and try again."
                )
            )
            return

        settings.reload()
        old_prefix: str = settings["commands.prefix"]

        if old_prefix == new_prefix:
            await ctx.reply(
                embed=self.bot.error_embed(
                    "That prefix is already in use dumbo. Try something else",
                )
            )
            return

        async with aiofiles.open("config.toml", "r") as f:
            contents = await f.read()

        settings_data = toml.loads(contents)
        settings_data["commands"]["prefix"] = new_prefix

        async with aiofiles.open("config.toml", "w") as f:
            await f.write(toml.dumps(settings_data))

        await ctx.reply(
            embed=Embed(
                description=f"{SETTINGS_INFO} Prefix for this server successfully changed to: `{new_prefix}`"
            )
        )


async def setup(bot: Riko) -> None:
    await bot.add_cog(Prefix(bot))
