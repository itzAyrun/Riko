import random

from discord.ext import commands
from discord.ext.commands import BucketType, Cog, Context

from riko import Riko

EIGHTBALL_RESPONSES = []


class Eightball(Cog):
    def __init__(self, bot: Riko) -> None:
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=BucketType.user)
    async def eightball(self, ctx: Context, *, question: str) -> None:
        response = random.choice(EIGHTBALL_RESPONSES)
        await ctx.reply(
            f"{ctx.author.name}'s Question: **{question}**\nMy Honest Answer: **{response}**"
        )


async def setup(bot: Riko) -> None:
    await bot.add_cog(Eightball(bot))
