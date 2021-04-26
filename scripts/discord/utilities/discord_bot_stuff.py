from scripts.discord.bot_holder import BotHolder
from discord.ext.commands.bot import Bot
from discord.channel import TextChannel
from discord.user import User
from scripts.discord.errors.discord_system_errors import BotIsNotReady


class DiscordStuffSystem:
    bot: Bot = BotHolder.bot

    @classmethod
    async def get_user_name_by_id(cls, id: int) -> str:
        if not cls.bot.is_ready():
            raise BotIsNotReady
        try:
            user: User = await cls.bot.fetch_user(id)
            return user.name
        except Exception as err:
            raise

    @classmethod
    async def get_channel_by_id(cls, id: int) -> TextChannel:
        if not cls.bot.is_ready():
            raise BotIsNotReady
        try:
            channel: TextChannel = await cls.bot.fetch_channel(id)
            return channel
        except Exception as err:
            raise

    @classmethod
    def check_if_bot_is_ready(cls) -> bool:
        if cls.bot.is_ready():
            return True
        return False
