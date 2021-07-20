import logging
import os
import sys

import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from discord.ext.commands.context import Context
from pretty_help import PrettyHelp

from core.config import Configuration


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

default_extensions = ["cogs."+i.replace(".py", "")
                      for i in os.listdir("cogs") if i.endswith(".py")]


def get_prefix(bot, msg):
    return commands.when_mentioned_or(bot.configs[msg.guild.id]["prefix"])(bot, msg)


class Bot(AutoShardedBot):
    def __init__(self):   
        super().__init__(
            command_prefix=get_prefix,
            help_command=PrettyHelp(
                color=0xffff00, show_index=True, sort_commands=True),
            intents=discord.Intents.all()
        )
        self.configs = {}
        self.__version__ = "0.0.1alpha"


bot = Bot()


@bot.command(name="reload")
@commands.is_owner()
async def reload_extension(ctx: Context, extension: str):
    bot.reload_extension(extension)
    logging.info(f"{extension} reloaded")
    embed = discord.Embed(
        color=0xffff00, description=f"{extension} reloaded")
    embed.set_author(name="Reload", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)


@bot.command(name="load")
@commands.is_owner()
async def reload_extension(ctx: Context, extension: str):
    bot.load_extension(extension)
    logging.info(f"{extension} loaded")
    embed = discord.Embed(
        color=0xffff00, description=f"{extension} loaded")
    embed.set_author(name="Load", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)


@bot.command(name="unload")
@commands.is_owner()
async def reload_extension(ctx: Context, extension: str):
    bot.unload_extension(extension)
    logging.info(f"{extension} unloaded")
    embed = discord.Embed(
        color=0xffff00, description=f"{extension} unloaded")
    embed.set_author(name="Unload", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    for extension in default_extensions:
        bot.load_extension(extension)
        logging.info(f"{extension} loaded")

    bot.run(os.environ["REICHBOT"])
