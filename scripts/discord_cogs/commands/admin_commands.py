from discord.ext import commands
from scripts.managingRolesScript import RolesKOX


class AdminCommands(commands.Cog):

    """Category documentations"""

    def __init__(self):
        pass

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['Admin'])
    async def do_nothing(self, ctx):
        """Nic nie robi"""
        await ctx.send('No i nic')

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['Admin'])
    async def update_data_schemes(self, ctx):

        await ctx.send('Done')
