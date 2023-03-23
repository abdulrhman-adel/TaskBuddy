import nextcord
from nextcord import Member, Interaction
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord.utils import get


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def addRole(self, ctx, user: nextcord.Member, *, role: nextcord.Role):
        if role in user.roles:
            await ctx.send(f"{user.mention} already has that role")
        else:
            await user.add_roles(role)
            await ctx.send(f"{user.mention} has been given the role {role.mention}")

    @addRole.error
    async def addRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def removeRole(self, ctx, user: nextcord.Member, *, role: nextcord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"{user.mention} has had the role {role.mention} removed")
        else:
            await ctx.send(f"{user.mention} does not have that role")

    @removeRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command")


def setup(bot):
    bot.add_cog(Admin(bot))
