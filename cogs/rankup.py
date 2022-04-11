import discord
from discord.ext import commands

import json

from constants import roles, channels, datetime
from utils import checks


class Rankup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("./config/rankup.json", "r", encoding="utf-8") as json_config_file:
            self.rankup_rules = json.load(json_config_file)

        self.ranked_roles = list(self.rankup_rules.keys())

    def _get_user_ranked_roles(self, user):
        roles = []
        for role in user.roles:
            if role.name in self.ranked_roles:
                roles.append(role)
        return roles

    def _get_highest_ranked_role(self, user, exclued_roles = []):
        user_ranked_roles = self._get_user_ranked_roles(user)
        user_roles = [r.name for r in user_ranked_roles]
        for ranked_role in self.ranked_roles[::-1]:
            if ranked_role in user_roles and ranked_role not in exclued_roles:
                return ranked_role

    @commands.command()
    @commands.has_any_role(roles.APSOLVENT, roles.IMATRIKULANT)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    async def imatrikulant(self, ctx):
        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        imatrikulant_role = discord.utils.get(ctx.guild.roles, name=roles.IMATRIKULANT)
        apsolvet_role = discord.utils.get(ctx.guild.roles, name=roles.APSOLVENT)

        await ctx.author.add_roles(imatrikulant_role)
        await ctx.author.remove_roles(apsolvet_role)
        await ctx.author.add_roles(registrovan_role)

        emoji = ":moneybag:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} je imatrikulant {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases=["imatrikulant+"])
    @commands.has_any_role(roles.APSOLVENT, roles.IMATRIKULANT)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    async def imatrikulant_(self, ctx):
        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        imatrikulant_role = discord.utils.get(ctx.guild.roles, name=roles.IMATRIKULANT)
        apsolvet_role = discord.utils.get(ctx.guild.roles, name=roles.APSOLVENT)

        highest_role = self._get_highest_ranked_role(ctx.author, [roles.APSOLVENT, roles.IMATRIKULANT])
        lower_role_name = self.rankup_rules[highest_role]["Previous"]

        if lower_role_name is not None:
            lower_role = discord.utils.get(ctx.guild.roles, name=lower_role_name)
            await ctx.author.remove_roles(lower_role)

        try:
            await ctx.author.add_roles(imatrikulant_role)
            await ctx.author.remove_roles(apsolvet_role)
        except Exception:
            pass

        await ctx.author.add_roles(registrovan_role)

        emoji = ":moneybag:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} je imatrikulant {emoji}"
        )
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    @commands.has_any_role(roles.TRECA_GODINA, roles.CETVRTA_GODINA)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    @checks.in_date_range(datetime.START_DATE_APSOLVENT, datetime.STOP_DATE_APSOLVENT)
    async def apsolvent(self, ctx):
        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        apsolvet_role = discord.utils.get(ctx.guild.roles, name=roles.APSOLVENT)

        await ctx.author.add_roles(apsolvet_role)
        await ctx.author.add_roles(registrovan_role)

        emoji = ":money_mouth:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} je apsolvent {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases=["apsolvent+"])
    @commands.has_any_role(roles.TRECA_GODINA, roles.CETVRTA_GODINA)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    @checks.in_date_range(datetime.START_DATE_APSOLVENT, datetime.STOP_DATE_APSOLVENT)
    async def apsolvent_(self, ctx):
        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        apsolvet_role = discord.utils.get(ctx.guild.roles, name=roles.APSOLVENT)

        highest_role = self._get_highest_ranked_role(ctx.author, [roles.APSOLVENT])

        lower_role_name = self.rankup_rules[highest_role]["Previous"]

        if lower_role_name is not None:
            lower_role = discord.utils.get(ctx.guild.roles, name=lower_role_name)
            await ctx.author.remove_roles(lower_role)

        try:
            await ctx.author.add_roles(apsolvet_role)
        except Exception:
            pass

        await ctx.author.add_roles(registrovan_role)

        emoji = ":money_mouth:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} je apsolvent {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases=["alumni", "alumna", "diploma", "diplomirao", "diplomirala"])
    @commands.has_any_role(roles.TRECA_GODINA, roles.CETVRTA_GODINA)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    async def alum(self, ctx):
        alum_role = discord.utils.get(ctx.guild.roles, name=roles.ALUMNI)
        await ctx.author.add_roles(alum_role)

        ranked_role = self._get_user_ranked_roles(ctx.author)
        for role in ranked_role:
            await ctx.author.remove_roles(role)

        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = ":mortar_board: " + ctx.author.mention + " je diplomirao/diplomirala :mortar_board:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases=["ocistio", "ocistila"])
    @commands.has_any_role(roles.PRVA_GODINA, roles.DRUGA_GODINA, roles.TRECA_GODINA)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    @checks.in_date_range(datetime.START_DATE_CISTA, datetime.STOP_DATE_CISTA)
    async def cista(self, ctx):
        highest_role = self._get_highest_ranked_role(ctx.author)

        ranked_role = self._get_user_ranked_roles(ctx.author)
        for role in ranked_role:
            await ctx.author.remove_roles(role)

        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        next_role = discord.utils.get(ctx.guild.roles, name=self.rankup_rules[highest_role]["Next"])

        await ctx.author.add_roles(next_role)
        await ctx.author.add_roles(registrovan_role)

        emoji = ":tada:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} je ocistio/ocistila {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    @commands.has_any_role(roles.PRVA_GODINA, roles.DRUGA_GODINA, roles.TRECA_GODINA)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    @checks.in_date_range(datetime.START_DATE_USLOV, datetime.STOP_DATE_USLOV)
    async def uslov(self, ctx):
        highest_role = self._get_highest_ranked_role(ctx.author)

        ranked_role = self._get_user_ranked_roles(ctx.author)
        for role in ranked_role:
            if role.name != highest_role:
                await ctx.author.remove_roles(role)

        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        next_role = discord.utils.get(ctx.guild.roles, name=self.rankup_rules[highest_role]["Next"])

        await ctx.author.add_roles(next_role)
        await ctx.author.add_roles(registrovan_role)

        emoji = ":tada:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} je ispunio/ispunila uslov {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases=["obnovio", "obnovila"])
    @commands.has_any_role(roles.PRVA_GODINA, roles.DRUGA_GODINA, roles.TRECA_GODINA)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    @checks.in_date_range(datetime.START_DATE_OBNOVA, datetime.STOP_DATE_OBNOVA)
    async def obnova(self, ctx):
        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        await ctx.author.add_roles(registrovan_role)

        emoji = ":face_with_symbols_over_mouth:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} se je obnovio/obnovila {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    @commands.has_any_role(roles.PRVA_GODINA, roles.DRUGA_GODINA, roles.TRECA_GODINA)
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    @checks.doesnt_have_any_role(roles.REGISTROVAN)
    @checks.in_date_range(datetime.START_DATE_KOLIZIJA, datetime.STOP_DATE_KOLIZIJA)
    async def kolizija(self, ctx):
        highest_role = self._get_highest_ranked_role(ctx.author)

        registrovan_role = discord.utils.get(ctx.guild.roles, name=roles.REGISTROVAN)
        next_role = discord.utils.get(ctx.guild.roles, name=self.rankup_rules[highest_role]["Kolizija"])

        await ctx.author.add_roles(next_role)
        await ctx.author.add_roles(registrovan_role)

        emoji = ":money_with_wings:"
        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{emoji} {ctx.author.mention} je upisao/upisala koliziju {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    async def ispis(self, ctx):
        await ctx.author.kick(reason = "Ispis")

        embed = discord.Embed(
            colour = discord.Colour.gold(),
            description = f"{ctx.author.mention} se ispisao/ispisala"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Rankup(bot))
