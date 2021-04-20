from discord.ext import commands


def check_if_it_is_me(ctx):
    return True


class ZefirCommands(commands.Cog):

    """Category documentations"""

    def __init__(self):
        pass

    @commands.command(pass_context=True)
    @commands.check(check_if_it_is_me)
    async def scan_for_users(self, ctx):

        await ctx.channel.send(f'Done')



