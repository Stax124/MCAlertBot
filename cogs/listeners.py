import discord
import logging
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands
from discord.member import Member
from discord.user import User
from discord.utils import get
from core.config import Configuration


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        logging.info("Bot sucessfully connected to Discord servers")

    @commands.Cog.listener()
    async def on_connected(self):
        logging.info("Connected to Discord servers")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Guilds joined: {len(self.bot.guilds)}")

        for guild in self.bot.guilds:
            config = Configuration(guild.id)
            config.load()
            self.bot.configs[guild.id] = config

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.info("Bot lost connection to Discord servers")

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        if self.bot.configs[member.guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[member.guild.id]["log_channel"])

            embed = discord.Embed(color=0xff0000)
            embed.set_author(name="Member left",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=member.display_name)
            embed.add_field(name="Joined at",
                            value=member.joined_at.strftime(r'%c'))
            embed.add_field(name="ID", value=member.id)
            embed.set_thumbnail(url=member.avatar_url)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member: Member):
        if self.bot.configs[guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[guild.id]["log_channel"])

            embed = discord.Embed(color=0xff0000)
            embed.set_author(name="Member banned",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=member.display_name)
            embed.add_field(name="ID", value=member.id)
            embed.set_thumbnail(url=member.avatar_url)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member: Member):
        if self.bot.configs[guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[guild.id]["log_channel"])

            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name="Member unbanned",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=member.display_name)
            embed.add_field(name="ID", value=member.id)
            embed.set_thumbnail(url=member.avatar_url)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if self.bot.configs[member.guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[member.guild.id]["log_channel"])

            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name="Member joined",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=member.display_name)
            embed.add_field(name="ID", value=member.id)
            embed.set_thumbnail(url=member.avatar_url)

            await channel.send(embed=embed)

        if self.bot.configs[member.guild.id]["autorole"] != None:
            await member.add_roles(
                get(member.guild.roles, id=self.bot.configs[member.guild.id]["autorole"]), reason="Autorole")

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if self.bot.configs[before.guild.id]["log_channel"] != None:
            send = False
            embed = discord.Embed(color=0xffa500, description=after.mention)
            embed.set_author(name="Member updated",
                             icon_url=self.bot.user.avatar_url)

            for item in before.__slots__:
                if not (item.startswith("_") or item == "activities"):
                    if before.__getattribute__(item) != after.__getattribute__(item):
                        send = True
                        embed.add_field(
                            name=item, value=f"{before.__getattribute__(item)} -> {after.__getattribute__(item)}")

            if send:
                embed.set_thumbnail(url=after.avatar_url)
                channel = self.bot.get_channel(
                    self.bot.configs[before.guild.id]["log_channel"])
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before: Member, after: Member):
        if self.bot.configs[before.guild.id]["log_channel"] != None:
            send = False
            embed = discord.Embed(color=0xffa500, description=after.mention)
            embed.set_author(name="User updated",
                             icon_url=self.bot.user.avatar_url)

            for item in before.__slots__:
                if not (item.startswith("_") or item == "activities"):
                    send = True
                    if before.__getattribute__(item) != after.__getattribute__(item):
                        embed.add_field(
                            name=item, value=f"{before.__getattribute__(item)} -> {after.__getattribute__(item)}")

            if send:
                embed.set_thumbnail(url=after.avatar_url)
                channel = self.bot.get_channel(
                    self.bot.configs[before.guild.id]["log_channel"])
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        if self.bot.configs[role.guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[role.guild.id]["log_channel"])

            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name="Role created",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=role.name)
            embed.add_field(name="ID", value=role.id)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        if self.bot.configs[role.guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[role.guild.id]["log_channel"])

            embed = discord.Embed(color=0xff0000)
            embed.set_author(name="Role deleted",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=role.name)
            embed.add_field(name="ID", value=role.id)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        if self.bot.configs[before.guild.id]["log_channel"] != None:
            embed = discord.Embed(color=0xffa500)
            embed.set_author(name="Role updated",
                             icon_url=self.bot.user.avatar_url)

            for item in before.__slots__:
                if before.__getattribute__(item) != after.__getattribute__(item):
                    embed.add_field(
                        name=item, value=f"{before.__getattribute__(item)} -> {after.__getattribute__(item)}")

            channel = self.bot.get_channel(
                self.bot.configs[before.guild.id]["log_channel"])
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if self.bot.configs[channel.guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[channel.guild.id]["log_channel"])

            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name="Channel created",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=channel.name)
            embed.add_field(name="ID", value=channel.id)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        if self.bot.configs[channel.guild.id]["log_channel"] != None:
            channel = self.bot.get_channel(
                self.bot.configs[channel.guild.id]["log_channel"])

            embed = discord.Embed(color=0xff0000)
            embed.set_author(name="Channel removed",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Name", value=channel.name)
            embed.add_field(name="ID", value=channel.id)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        if self.bot.configs[before.guild.id]["log_channel"] != None:
            embed = discord.Embed(color=0xffa500)
            embed.set_author(name="Channel updated",
                             icon_url=self.bot.user.avatar_url)

            for item in before.__slots__:
                if item != "_overwrites":
                    if before.__getattribute__(item) != after.__getattribute__(item):
                        embed.add_field(
                            name=item, value=f"{before.__getattribute__(item)} -> {after.__getattribute__(item)}")

            channel = self.bot.get_channel(
                self.bot.configs[before.guild.id]["log_channel"])
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Listeners(bot))
