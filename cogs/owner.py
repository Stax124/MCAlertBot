import discord
import logging
import sys
from discord.enums import Status
from discord.ext import commands
from discord.ext.commands.context import Context
from core.shared import confirm


class Owner(commands.Cog):
    "Owner commands"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown", help="Terminate the process", pass_context=True)
    @commands.is_owner()
    async def shutdown(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Terminate process ?")
        if not confirmed:
            return

        logging.warning("Shutting down bot")
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description="✅ Shutting down..."
        )
        embed.set_author(name="Shutdown", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        logging.info("Shutting down...")

        await self.bot.change_presence(activity=discord.Game(name=f"Shutting down..."), status=Status.offline)
        sys.exit()


def setup(bot):
    bot.add_cog(Owner(bot))
