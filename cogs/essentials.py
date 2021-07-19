import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from core.shared import confirm
from typing import Union


class Essentials(commands.Cog):
    "Esential functions"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", help="Delete messages from channel")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: Context, messages: int = 100):
        if await confirm(self.bot, ctx, message=f"Clean {messages} messages ?"):
            await ctx.channel.purge(limit=messages)

    @commands.command(name="autorole", help="Set default role after member joins")
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx: Context, role: Union[discord.Role, None]):
        if role == None:
            self.bot.configs[ctx.guild.id]["autorole"] = None
        else:
            _id = role.id
            self.bot.configs[ctx.guild.id]["autorole"] = _id

        self.bot.configs[ctx.guild.id].save()

        embed = discord.Embed(
            color=0xffff00, description=f"Auto-role set to {role.mention if role != None else 'None'}")
        embed.set_author(name="Auto-role", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Essentials(bot))
