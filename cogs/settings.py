import json
from discord.ext import commands
from discord.ext.commands.context import Context
from core.shared import confirm


class Settings(commands.Cog):
    "Settings"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="config", help="Dump config for your server")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context):
        await ctx.send(json.dumps(self.bot.configs[ctx.guild.id].config))

    @commands.command(name="version")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context):
        await ctx.send(self.bot.__version__)
        
    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, prefix: str):
        if await confirm(self.bot, ctx, message=f"Set audit channel to {ctx.channel.mention} ?"):
            self.bot.configs[ctx.guild.id]["prefix"] = prefix
            self.bot.configs[ctx.guild.id].save()
        


def setup(bot):
    bot.add_cog(Settings(bot))
