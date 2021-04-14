import discord
from discord.ext import commands
from discord.ext import tasks

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import datetime
import json

from models.user import User
import models.base as base

from utils import misc
from utils import randemoji

def is_in_channel(ctx):
    return ctx.channel.name == 'bot-commands' or ctx.channel.name == 'logger'
    

class Rankup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.role_name = "Registrovan"
        self.role = misc.getRoleByName(self.client, self.role_name)

        with open(".\\config\\rankup.json", "r", encoding="utf-8") as jsonConfigFile:
            self.rankup_rules = json.load(jsonConfigFile)

        self.ranked_roles = list(self.rankup_rules.keys())
        self.session = base.Session()

    def get_role(self, role_name):
        return misc.getRoleByName(self.client, role_name)

    def get_user_roles(self, user):
        return [role.name for role in user.roles]

    def get_user_ranked_roles(self, user):
        roles = []
        user_roles = self.get_user_roles(user)
        for role in user_roles:
            if role in self.ranked_roles:
                roles.append(self.get_role(role))
        return roles

    def get_highest_ranked_role(self, user, exclued_roles = []):
        user_roles = self.get_user_roles(user)
        for ranked_role in self.ranked_roles[::-1]:
            if ranked_role in user_roles and ranked_role not in exclued_roles:
                return ranked_role

    @commands.command()
    @commands.check(is_in_channel) 
    @commands.has_any_role("Imatrikulant") 
    async def imatrikulant(self, ctx):
        registrovan_role = self.get_role("Registrovan")
        imatrikulant_role = self.get_role("Imatrikulant")
        apsolvet_role = self.get_role("Apsolvent")

        await ctx.author.add_roles(imatrikulant_role)
        await ctx.author.remove_roles(apsolvet_role)
        await ctx.author.add_roles(registrovan_role)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je imatrikulant :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
        
    @commands.command(aliases=["imatrikulant+"])
    @commands.has_any_role("Apsolvent", "Imatrikulant")
    @commands.check(is_in_channel) 
    async def imatrikulant_(self, ctx):
        registrovan_role = self.get_role("Registrovan")
        imatrikulant_role = self.get_role("Imatrikulant")
        apsolvet_role = self.get_role("Apsolvent")

        lower_role_name = "" 
        highest_role = self.get_highest_ranked_role(ctx.author, ["Apsolvent", "Imatrikulant"])
        
        if highest_role == "Četvrta godina":
            lower_role_name = "Treća godina"
        elif highest_role == "Treća godina":
            lower_role_name = "Druga godina"

        if lower_role_name != "":
            lower_role = self.get_role(lower_role_name)
            await ctx.author.remove_roles(lower_role)

        try:
            await ctx.author.add_roles(imatrikulant_role)
            await ctx.author.remove_roles(apsolvet_role)
        except:
            pass

        await ctx.author.add_roles(registrovan_role)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je imatrikulant :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        

        await ctx.send(embed = embed)
    
    @commands.command()
    @commands.has_any_role("Treća godina")
    @commands.check(is_in_channel) 
    async def apsolvent(self, ctx):
        registrovan_role = self.get_role("Registrovan")
        apsolvet_role = self.get_role("Apsolvent")

        await ctx.author.add_roles(apsolvet_role)
        await ctx.author.add_roles(registrovan_role)
        
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je apsolvent :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        

        await ctx.send(embed = embed)

    @commands.command(aliases=["apsolvent+"])
    @commands.has_any_role("Treća godina", "Četvrta godina")
    @commands.check(is_in_channel) 
    async def apsolvent_(self, ctx):
        registrovan_role = self.get_role("Registrovan")
        apsolvet_role = self.get_role("Apsolvent")

        lower_role_name = "" 
        highest_role = self.get_highest_ranked_role(ctx.author, ["Apsolvent"])
        
        if highest_role == "Četvrta godina":
            lower_role_name = "Treća godina"
        elif highest_role == "Treća godina":
            lower_role_name = "Druga godina"

        if lower_role_name != "":
            lower_role = self.get_role(lower_role_name)
            await ctx.author.remove_roles(lower_role)

        try:
            await ctx.author.add_roles(apsolvet_role)
        except:
            pass

        await ctx.author.add_roles(registrovan_role)

        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je apsolvent :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        

        await ctx.send(embed = embed)

    
    @commands.command(aliases=["diplomirao", "diplomirala"])
    @commands.has_any_role("Treća godina", "Četvrta godina")
    @commands.check(is_in_channel)
    async def diploma(self, ctx):
        
        await ctx.author.kick(reason = "Diplomirao/Diplomirala")
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :mortar_board: " + ctx.author.mention + " je diplomirao/diplomirala :mortar_board:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    @commands.command(aliases=["alumni", "alumna"])
    @commands.has_any_role("Treća godina", "Četvrta godina") 
    @commands.check(is_in_channel) 
    async def alum(self, ctx):
        
        alum_role = self.get_role("Alumni")
        await ctx.author.add_roles(alum_role)

        ranked_role = self.get_user_ranked_roles(ctx.author)
        for role in ranked_role:
            await ctx.author.remove_roles(role)

        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :mortar_board: " + ctx.author.mention + " je diplomirao/diplomirala :mortar_board:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
    
    @commands.command(aliases=["ocistio", "ocistila"])
    @commands.has_any_role("Prva godina", "Druga godina", "Treća godina")
    @commands.check(is_in_channel) 
    async def cista(self, ctx):
        highest_role = self.get_highest_ranked_role(ctx.author)

        ranked_role = self.get_user_ranked_roles(ctx.author)
        for role in ranked_role:
            await ctx.author.remove_roles(role)

        next_role = self.get_role(self.rankup_rules[highest_role]["Next"])
        registrovan_role = self.get_role("Registrovan")
        await ctx.author.add_roles(next_role)
        await ctx.author.add_roles(registrovan_role)

        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je ocistio/ocistila :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    
    @commands.command()
    @commands.has_any_role("Prva godina", "Druga godina", "Treća godina")
    @commands.check(is_in_channel) 
    async def uslov(self, ctx):
        highest_role = self.get_highest_ranked_role(ctx.author)

        ranked_role = self.get_user_ranked_roles(ctx.author)
        for role in ranked_role:
            if role.name != highest_role:
                await ctx.author.remove_roles(role)

        next_role = self.get_role(self.rankup_rules[highest_role]["Next"])
        registrovan_role = self.get_role("Registrovan")

        await ctx.author.add_roles(next_role)
        await ctx.author.add_roles(registrovan_role)


        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je ispunio/ispunila uslov :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
        

    @commands.command(aliases=["obnovio", "obnovila"])
    @commands.has_any_role("Prva godina", "Druga godina", "Treća godina")
    @commands.check(is_in_channel) 
    async def obnova(self, ctx):
        
        registrovan_role = self.get_role("Registrovan")
        await ctx.author.add_roles(next_role)
        
        emoji = randemoji.Get()
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = f"\n {emoji} {ctx.author.mention} se je obnovio/obnovila {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    @commands.command()
    @commands.has_any_role("Prva godina", "Druga godina", "Treća godina")
    @commands.check(is_in_channel) 
    async def kolizija(self, ctx):
        highest_role = self.get_highest_ranked_role(ctx.author)

        next_role = self.get_role(self.rankup_rules[highest_role]["Kolizija"])
        registrovan_role = self.get_role("Registrovan")
        
        await ctx.author.add_roles(next_role)
        await ctx.author.add_roles(registrovan_role)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je upisao/upisala koliziju :tada:"
        )
        
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        
        await ctx.send(embed = embed)


    @commands.command()
    @commands.check(is_in_channel) 
    async def ispis(self, ctx):
        await ctx.author.kick(reason = "Ispis")
        emoji = randemoji.Get()
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = f"\n {emoji} {ctx.author.mention} se ispisao/ispisala {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Rankup(client))