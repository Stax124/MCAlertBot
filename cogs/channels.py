from discord.ext import commands
from discord.ext.commands.context import Context
from core.shared import confirm


class Channels(commands.Cog):
    "Managing channels"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="log-setup")
    @commands.has_permissions(administrator=True)
    async def audit_channel(self, ctx: Context):
        if await confirm(self.bot, ctx, message=f"Set channel to {ctx.channel.mention} ?"):
            self.bot.configs[ctx.guild.id]["log_channel"] = ctx.channel.id
            self.bot.configs[ctx.guild.id].save()


def setup(bot):
    bot.add_cog(Channels(bot))
