import discord
from constants import roles


def get_member_roles_as_string(member: discord.Member):
    member_roles: str = ""
    for role in member.roles:
        if role.name != roles.EVERYONE:
            member_roles += role.mention + " "
    return member_roles
