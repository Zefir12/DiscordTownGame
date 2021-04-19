import discord
from discord.ext import commands, tasks
import datetime
import time


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            print(error, ctx.author, ctx.guild.name, datetime.datetime.now())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('!'):
            pass
            #await message.delete()
        if message.content == 'k2':
            await message.channel.send('affirmative!')
        if message.content.lower().find('kurwa') != -1:
            for emoji in message.guild.emojis:
                if emoji.name == 'monkaS':
                    await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        pass
