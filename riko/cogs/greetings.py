import random

from discord.ext import commands
from discord.ext.commands import BucketType, Context, Cog

from riko import Riko
from config import settings


class Greetings(Cog):
    def __init__(self, bot: Riko) -> None:
        self.bot = bot

    @commands.group(aliases=["hi", "hey"])
    @commands.cooldown(
        rate=1, per=settings["commands.hello.cooldown"], type=BucketType.user
    )
    async def hello(self, ctx: Context) -> None:
        settings.reload()
        await ctx.reply(random.choice(settings["commands.hello.responses"]))


async def setup(bot: Riko) -> None:
    await bot.add_cog(Greetings(bot))
