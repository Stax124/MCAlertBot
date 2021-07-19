from discord.ext.commands import Bot
from discord.ext.commands.context import Context
import discord
import asyncio
from mcstatus import MinecraftServer


async def confirm(bot: Bot, ctx: Context, message: str, timeout: int = 20, author: str = "Confirm"):
    try:
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description=message
        )
        embed.set_author(name=author, icon_url=bot.user.avatar_url)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

        reaction, _ = await bot.wait_for('reaction_add', timeout=timeout, check=check)
        if reaction.emoji == '❌':
            await msg.delete()
            return False
        elif reaction.emoji == '✅':
            await msg.delete()
            return True
    except asyncio.TimeoutError:
        await msg.delete()
        return False


async def get_threats(bot, guild_id: int) -> tuple:
    threats = []
    moderators = []

    server = MinecraftServer(
        bot.configs[guild_id]["minecraft_server"])
    query = await server.async_query()
    names = query.players.names

    warnings = bot.configs[guild_id]["minecraft_warnings"]
    alerts = bot.configs[guild_id]["minecraft_alerts"]

    # Increment threats by one for name in names if name is in alerts
    for name in names:
        if name in alerts:
            threats.append(name)

    # Increment moderators by one for name in names if name is in warnings
    for name in names:
        if name in warnings:
            moderators.append(name)

    return (threats, moderators)


class Codes():
    GREEN = ":green_square: CODE GREEN: No current threats, encounters of danger very unlikely."
    YELLOW = ":yellow_square: CODE YELLOW: Possible threats online, be ready to defend or be on standby for an attack."
    ORANGE = ":orange_square: CODE ORANGE: Threats online, danger levels fairly high. Attacks will likely take place."
    RED = ":red_square: CODE RED: Serious danger levels, anyone who is underprepared should NOT be online for any reason."


def get_code(bot: Bot, guild_id: int, threats: int, moderators: int):

    if bot.configs[guild_id]["raid_ongoing"]:
        return Codes.RED
    else:
        if len(threats) == 0:
            return Codes.GREEN
        elif len(threats) == 1:
            return Codes.YELLOW
        elif len(threats) >= 3:
            return Codes.ORANGE
