from discord.ext import commands
import discord


class BotHolder():
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
