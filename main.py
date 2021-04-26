import discord
from certs_and_tokens import TOKENS
from scripts.discord.commands.moderator_commands import ModeratorCommands
from scripts.discord.commands.admin_commands import AdminCommands
from scripts.discord.commands.user_commands import UserCommands
from scripts.discord.commands.zefir_commands import ZefirCommands
from scripts.discord.tasks.timers import Timers
from scripts.discord.listeners.listeners import Listeners
from discord.ext import commands
from scripts.discord.bot_holder import BotHolder


# bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

token = TOKENS.discord_bot_token

bot = BotHolder.bot

bot.add_cog(UserCommands(bot))
bot.add_cog(Timers())
bot.add_cog(Listeners(bot))


bot.run(token)


