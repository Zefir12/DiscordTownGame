from scripts.discord.bot_holder import BotHolder
from discord.ext.commands.bot import Bot
from discord.user import User
from scripts.discord.errors.discord_system_errors import BotIsNotReady


bot: Bot = BotHolder.bot


class DiscordStuffSystem:

    @classmethod
    async def get_user_name_by_id(cls, id: int) -> str:
        if not bot.is_ready():
            raise BotIsNotReady
        try:
            user: User = await bot.fetch_user(id)
            return user.name
        except Exception as err:
            raise
