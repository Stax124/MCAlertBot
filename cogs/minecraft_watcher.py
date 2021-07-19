import asyncio
import discord
import DiscordUtils
from core.shared import confirm, get_threats
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.utils import get
from mcstatus import MinecraftServer


class MinecraftWatcher(commands.Cog):
    "Watching and alerting"

    def __init__(self, bot):
        self.bot = bot

    # Set server that will be watched
    @commands.command(name="server-watch")
    @commands.has_permissions(administrator=True)
    async def server_watch(self, ctx: Context, *, server: str):
        self.bot.configs[ctx.guild.id]["minecraft_server"] = server
        self.bot.configs[ctx.guild.id].save()

        embed = discord.Embed(
            color=0xffff00, description=f"Watching {server}")
        embed.set_author(name="Server-watch",
                         icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # Query the selected server and get stats
    @commands.command(name="server-query")
    async def server_querry(self, ctx: Context):
        server = MinecraftServer(
            self.bot.configs[ctx.guild.id]["minecraft_server"])
        query = await server.async_query()
        status = await server.async_status()

        num_of_players, max_players, ping = query.players.online, query.players.max, status.latency

        embed = discord.Embed(color=0xffff00)
        embed.set_author(name=self.bot.configs[ctx.guild.id]["minecraft_server"],
                         icon_url=self.bot.user.avatar_url)
        embed.add_field(
            name="Players", value=f"{num_of_players}/{max_players}")
        embed.add_field(name="Latency", value=f"{ping}ms")
        await ctx.send(embed=embed)

    # Get list of active players
    @commands.command(name="server-players")
    async def server_players(self, ctx: Context):
        server = MinecraftServer(
            self.bot.configs[ctx.guild.id]["minecraft_server"])
        query = await server.async_query()

        e_list = []
        msg = ""
        index = 1
        names = query.players.names
        names.sort()

        warnings = self.bot.configs[ctx.guild.id]["minecraft_warnings"]
        alerts = self.bot.configs[ctx.guild.id]["minecraft_alerts"]

        for name in names:
            msg += f"{index}. {':red_square:' if name in alerts else (':orange_square:' if name in warnings else ':green_square:')} [{name}](https://cs.namemc.com/search?q={name})\n"
            if index == 30:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=msg
                )
                embed.set_author(name="Players",
                                 icon_url=self.bot.user.avatar_url)
                e_list.append(embed)
                msg = ""
                index = 1
            else:
                index += 1

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description=msg
        )
        embed.set_author(name="Leaderboard", icon_url=self.bot.user.avatar_url)
        e_list.append(embed)

        paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
        paginator.remove_reactions = True
        await paginator.run(e_list)

    # Setup warnings
    @commands.command(name="server-warning")
    async def server_warning(self, ctx: Context, mode: str, *, name: str = ""):
        if mode == "add":
            self.bot.configs[ctx.guild.id]["minecraft_warnings"].append(name)
            self.bot.configs[ctx.guild.id].save()
            await ctx.send(f"{name} has been added to the list of warnings")
        elif mode == "remove":
            self.bot.configs[ctx.guild.id]["minecraft_warnings"].remove(name)
            self.bot.configs[ctx.guild.id].save()
            await ctx.send(f"{name} has been removed from the list of warnings")
        elif mode == "list":
            names = self.bot.configs[ctx.guild.id]["minecraft_warnings"]
            e_list = []
            msg = ""
            index = 1

            for name in names:
                msg += f"{index}. [{name}](https://en.namemc.com/search?q={name})\n"
                if index == 30:
                    embed = discord.Embed(
                        colour=discord.Colour.from_rgb(255, 255, 0),
                        description=msg
                    )
                    embed.set_author(name="Warning list",
                                     icon_url=self.bot.user.avatar_url)
                    e_list.append(embed)
                    msg = ""
                    index = 1
                else:
                    index += 1

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=msg
            )
            embed.set_author(name="Warning list",
                             icon_url=self.bot.user.avatar_url)
            e_list.append(embed)

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        else:
            await ctx.send("Invalid mode (add, remove, list)")

    # Setup alerts
    @commands.command(name="server-alert")
    async def server_alerts(self, ctx: Context, mode: str, *, name: str = ""):
        if mode == "add":
            self.bot.configs[ctx.guild.id]["minecraft_alerts"].append(name)
            self.bot.configs[ctx.guild.id].save()
            await ctx.send(f"{name} has been added to the list of alerts")
        elif mode == "remove":
            self.bot.configs[ctx.guild.id]["minecraft_alerts"].remove(name)
            self.bot.configs[ctx.guild.id].save()
            await ctx.send(f"{name} has been removed from the list of alerts")
        elif mode == "list":
            names = self.bot.configs[ctx.guild.id]["minecraft_alerts"]
            e_list = []
            msg = ""
            index = 1

            for name in names:
                msg += f"{index}. [{name}](https://cs.namemc.com/search?q={name})\n"
                if index == 30:
                    embed = discord.Embed(
                        colour=discord.Colour.from_rgb(255, 255, 0),
                        description=msg
                    )
                    embed.set_author(name="Alert list",
                                     icon_url=self.bot.user.avatar_url)
                    e_list.append(embed)
                    msg = ""
                    index = 1
                else:
                    index += 1

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=msg
            )
            embed.set_author(name="Alerts list",
                             icon_url=self.bot.user.avatar_url)
            e_list.append(embed)

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        else:
            await ctx.send("Invalid mode (add, remove, list)")

    # Setup role, that can give alerts
    @commands.command(name="server-member-role")
    @commands.has_permissions(administrator=True)
    async def server_member_role(self, ctx: Context, role: discord.Role):
        self.bot.configs[ctx.guild.id]["minecraft_member_role"] = role.id
        self.bot.configs[ctx.guild.id].save()
        await ctx.send(f"{role.name} has been set as the member role")

    # Alert all members when faction is under attack
    @commands.command(name="raid")
    async def raid(self, ctx: Context, *, message: str = ""):
        role = get(ctx.guild.roles,
                   id=self.bot.configs[ctx.guild.id]["minecraft_member_role"])
        if role in ctx.author.roles:
            threats, moderators = await get_threats(self.bot, ctx.guild.id)

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 0, 0),
                description=message
            )
            embed.add_field(name="Invoked by", value=ctx.author.mention)
            embed.add_field(name="Threats", value=threats)
            embed.add_field(name="Moderators", value=moderators)
            embed.set_author(name="RAID ONGOING",
                             icon_url=self.bot.user.avatar_url)

            channel = self.bot.get_channel(
                self.bot.configs[ctx.guild.id]["alert_channel"])
            await channel.send(embed=embed)
            await channel.send(role.mention)

            if not self.bot.configs[ctx.guild.id]["raid_ongoing"]:
                self.bot.configs[ctx.guild.id]["raid_ongoing"] = True
                await asyncio.sleep(3600)
                self.bot.configs[ctx.guild.id]["raid_ongoing"] = False
            else:
                await ctx.send("Raid is already in progress !")
                
                
    @commands.command(name="raid-supress")
    async def raid_supress(self, ctx: Context):
        role = get(ctx.guild.roles,
                   id=self.bot.configs[ctx.guild.id]["minecraft_member_role"])
        if role in ctx.author.roles:
            threats, moderators = await get_threats(self.bot, ctx.guild.id)

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(0, 255, 0),
                description="Raid is now supressed"
            )
            embed.add_field(name="Invoked by", value=ctx.author.mention)
            embed.add_field(name="Threats", value=threats)
            embed.add_field(name="Moderators", value=moderators)
            embed.set_author(name="RAID Supressed",
                             icon_url=self.bot.user.avatar_url)

            channel = self.bot.get_channel(
                self.bot.configs[ctx.guild.id]["alert_channel"])
            await channel.send(embed=embed)
            await channel.send(role.mention)

            if self.bot.configs[ctx.guild.id]["raid_ongoing"]:
                self.bot.configs[ctx.guild.id]["raid_ongoing"] = False

    @commands.command(name="threats")
    async def threats(self, ctx: Context):
        threats, moderators = await get_threats(self.bot, ctx.guild.id)

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 0, 0) if moderators > 0 else (
                discord.Colour.from_rgb(255, 255, 0) if threats > 0 else discord.Colour.from_rgb(0, 255, 0))
        )

        embed.add_field(name="Threats", value=threats)
        embed.add_field(name="Moderators", value=moderators)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MinecraftWatcher(bot))
