import discord
import asyncio
from datetime import datetime
from discord import player
from discord.utils import get
from core.shared import confirm, get_threats, get_code
from discord import channel
from discord.ext import commands, tasks
from discord.ext.commands.context import Context
from mcstatus import MinecraftServer


class Alerts(commands.Cog):
    "Watching for input and alerting"

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=60)
    async def check_for_code(self, ctx: Context, message_id: int):
        message = await ctx.fetch_message(message_id)

        threats, moderators = await get_threats(self.bot, ctx.guild.id)

        server = MinecraftServer(
            self.bot.configs[ctx.guild.id]["minecraft_server"])
        query = await server.async_query()
        
        color = discord.Color.from_rgb(255, 0, 0) if (len(moderators) > 0 or self.bot.configs[ctx.guild.id]["raid_ongoing"]) else (discord.Color.from_rgb(
            255, 255, 0) if len(threats) > 0 else discord.Color.from_rgb(0, 255, 0))

        code = get_code(self.bot, ctx.guild.id, threats, moderators)

        p_list = [mod + "\n" for mod in moderators]

        embed = discord.Embed(
            title="Status",
            description=code + "\n" + "Moderators: \n\n" +
            "".join(p_list) + "\n",
            color=color
        )
        embed.add_field(name="Threats online", value=len(threats))
        embed.add_field(
            name="Players", value=f"{query.players.online}/{query.players.max}")
        embed.add_field(name="Version", value=query.software.version)
        embed.add_field(name="Host", value=query.software.brand)
        embed.add_field(
            name="IP", value=self.bot.configs[ctx.guild.id]["minecraft_server"])
        embed.set_footer(text="Last update: " +
                         datetime.now().strftime(r"%H:%M:%S") + " UTC+2")
        await message.edit(message=None, embed=embed)

    @commands.command(name="alert-setup")
    @commands.has_permissions(administrator=True)
    async def alert_channel(self, ctx: Context):
        if await confirm(self.bot, ctx, message=f"Set channel to {ctx.channel.mention} ?"):
            self.bot.configs[ctx.guild.id]["alert_channel"] = ctx.channel.id
            self.bot.configs[ctx.guild.id].save()

    @commands.command(name="alert-message")
    @commands.has_permissions(administrator=True)
    async def alert_message(self, ctx: Context, priority: int, *, message: str):
        channel = self.bot.get_channel(
            self.bot.configs[ctx.guild.id]["alert_channel"])
        self.bot.configs[ctx.guild.id].save()

    # Set channel that will be used for alert codes
    @commands.command(name="codes-setup")
    @commands.has_permissions(administrator=True)
    async def server_watch(self, ctx: Context):
        if await confirm(self.bot, ctx, message=f"Set channel to {ctx.channel.mention} ?"):
            embed = discord.Embed(
                color=discord.Color.from_rgb(255, 255, 0),
                description="Setting up"
            )
            embed.set_author(name="Codes setup",
                             icon_url=self.bot.user.avatar_url)

            message = await ctx.send(embed=embed)
            self.bot.configs[ctx.guild.id]["codes_message_id"] = message.id
            self.bot.configs[ctx.guild.id].save()

            await self.check_for_code.start(ctx, message.id)

    @commands.command(name="get-code-tasks")
    @commands.has_permissions(administrator=True)
    async def get_code_tasks(self, ctx: Context):
        print("Getting task")
        tasks = self.check_for_code
        print(dir(tasks))


def setup(bot):
    bot.add_cog(Alerts(bot))