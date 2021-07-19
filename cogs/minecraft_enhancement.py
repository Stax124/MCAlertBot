import discord
import DiscordUtils
from discord.ext import commands
from discord.ext.commands.context import Context
from core.shared import confirm


class MinecraftEnhancement(commands.Cog):
    "Minecraft enhancement"

    def __init__(self, bot):
        self.bot = bot

    # Set server that will be watched
    @commands.command(name="enchant-god")
    @commands.has_permissions(administrator=True)
    async def enchant_god(self, ctx: Context):
        embed_helmet = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Protection IV](https://minecraft.fandom.com/wiki/Protection)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Respiration III](https://minecraft.fandom.com/wiki/Respiration)
[Aqua Affinity](https://minecraft.fandom.com/wiki/Aqua_Affinity)
[Thorns III](https://minecraft.fandom.com/wiki/Thorns) (Optional - Consumes extra Durability)
""")
        embed_helmet.set_author(name="Helmet",
                                icon_url=self.bot.user.avatar_url)

        embed_chest = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Protection IV](https://minecraft.fandom.com/wiki/Protection)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Thorns III](https://minecraft.fandom.com/wiki/Thorns) (Optional - Consumes extra Durability)
""")
        embed_chest.set_author(name="Chestplate",
                               icon_url=self.bot.user.avatar_url)

        embed_leggings = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Protection IV](https://minecraft.fandom.com/wiki/Protection)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Thorns III](https://minecraft.fandom.com/wiki/Thorns) (Optional - Consumes extra Durability)
""")
        embed_leggings.set_author(name="Leggings",
                                  icon_url=self.bot.user.avatar_url)

        embed_boots = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Protection IV](https://minecraft.fandom.com/wiki/Protection)
[Feather Falling IV](https://minecraft.fandom.com/wiki/Feather_Falling)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Depth Strider III](https://minecraft.fandom.com/wiki/Depth_Strider) or [Frost Walker II](https://minecraft.fandom.com/wiki/Frost_Walker) (Depth Strider overall preferred, as it is used in more circumstances)
[Soul Speed III](https://minecraft.fandom.com/wiki/Soul_Speed)
[Thorns III](https://minecraft.fandom.com/wiki/Thorns) (Optional - Consumes extra Durability)
""")
        embed_boots.set_author(name="Boots",
                               icon_url=self.bot.user.avatar_url)

        embed_sword = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Sharpness V](https://minecraft.fandom.com/wiki/Sharpness)
[Sweeping Edge III](https://minecraft.fandom.com/wiki/Sweeping_Edge)
[Looting III](https://minecraft.fandom.com/wiki/Looting)
[Fire Aspect II](https://minecraft.fandom.com/wiki/Fire_Aspect) (Optional - Enemy can set you on fire by hitting you)
[Knockback II](https://minecraft.fandom.com/wiki/Knockback) (Optional - Makes chasing an enemy more difficult, but running away easier)
""")
        embed_sword.set_author(name="Sword",
                               icon_url=self.bot.user.avatar_url)

        embed_axe = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Sharpness V](https://minecraft.fandom.com/wiki/Sharpness)
[Efficiency V](https://minecraft.fandom.com/wiki/Efficiency)
[Silk Touch](https://minecraft.fandom.com/wiki/Silk_Touch) or [Fortune III](https://minecraft.fandom.com/wiki/Fortune) (Silk touch is slighty better than fortune, but both are used in some circumstances)
""")
        embed_axe.set_author(name="Axe",
                             icon_url=self.bot.user.avatar_url)
        
        embed_bow = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending) or [Infinity](https://minecraft.fandom.com/wiki/Infinity)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Power V](https://minecraft.fandom.com/wiki/Power)
[Flame](https://minecraft.fandom.com/wiki/Silk_Touch)
[Punch II](https://minecraft.fandom.com/wiki/Efficiency) (Optional - Makes chassing enemies harder, but running away easier)
""")
        embed_bow.set_author(name="Bow",
                             icon_url=self.bot.user.avatar_url)
        
        embed_trident = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Loyalty III](https://minecraft.fandom.com/wiki/Power) and [Channeling](https://minecraft.fandom.com/wiki/Channeling) or only [Riptide III](https://minecraft.fandom.com/wiki/Riptide)
[Impaling V](https://minecraft.fandom.com/wiki/Impaling)
""")
        embed_trident.set_author(name="Trident",
                             icon_url=self.bot.user.avatar_url)
        
        embed_pickaxe = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Efficiency V](https://minecraft.fandom.com/wiki/Efficiency)
[Silk Touch](https://minecraft.fandom.com/wiki/Silk_Touch) or [Fortune III](https://minecraft.fandom.com/wiki/Fortune) (Silk touch is useful for ice, stone and ender chests, but otherwise fortune is better)
""")
        embed_pickaxe.set_author(name="Pickaxe",
                             icon_url=self.bot.user.avatar_url)
        
        embed_shovel = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
[Efficiency V](https://minecraft.fandom.com/wiki/Efficiency)
[Silk Touch](https://minecraft.fandom.com/wiki/Silk_Touch) or [Fortune III](https://minecraft.fandom.com/wiki/Fortune) (Silk touch is useful for grass and gravel, but fortune for flint)
""")
        embed_shovel.set_author(name="Shovel",
                             icon_url=self.bot.user.avatar_url)
        
        embed_elytra = discord.Embed(
            color=0xffff00, description=f"""
[Mending](https://minecraft.fandom.com/wiki/Mending)
[Unbreaking III](https://minecraft.fandom.com/wiki/Unbreaking)
""")
        embed_elytra.set_author(name="Elytra",
                             icon_url=self.bot.user.avatar_url)
        
        paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
        paginator.remove_reactions = True
        await paginator.run([embed_sword, embed_axe, embed_bow, embed_trident, embed_pickaxe, embed_shovel, embed_elytra] + [embed_helmet, embed_chest, embed_leggings, embed_boots])


def setup(bot):
    bot.add_cog(MinecraftEnhancement(bot))
