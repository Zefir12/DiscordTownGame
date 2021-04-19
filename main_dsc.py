import discord
from certs_and_tokens import TOKENS
from scripts.discord_cogs.commands.moderator_commands import ModeratorCommands
from scripts.discord_cogs.commands.admin_commands import AdminCommands
from scripts.discord_cogs.commands.user_commands import UserCommands
from scripts.discord_cogs.commands.zefir_commands import ZefirCommands
from scripts.discord_cogs.tasks.timers import Timers
from scripts.discord_cogs.listeners.listeners import Listeners
from discord.ext import commands
from discord_slash import SlashCommand


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

token = TOKENS.discord_bot_token


bot.add_cog(AdminCommands())
bot.add_cog(UserCommands(bot))
bot.add_cog(ZefirCommands())
bot.add_cog(ModeratorCommands(bot))
bot.add_cog(Timers(bot))
bot.add_cog(Listeners(bot))


bot.run(token)


