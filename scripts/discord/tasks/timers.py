from discord.ext import commands, tasks
from scripts.systems.high_level_systems.townManagingSystem import TownManagingSystem as tMS
from scripts.systems.middle_level_systems.eventSystem import EventSystem as evS
from scripts.systems.high_level_systems.embedSystem import EmbedSystem as embS
from scripts.systems.utilities.staticSavedChannelsAndGuilds import town_events_channel, town_events_guild
from scripts.discord.utilities.discord_bot_stuff import DiscordStuffSystem as dsS


class Timers(commands.Cog):
    def __init__(self):
        self.timer_5_s.start()
        self.event_channel = None

    @tasks.loop(seconds=5.0)
    async def timer_5_s(self):
        for user in tMS.get_users_currently_travelling():
            tMS.inc_user_travel_time(user.id, -5)
            tMS.settle_finished_user_on_destination(user.id)
        event = evS.get_random_event()
        if event is not False:
            event_result_list = evS.handle_event(event)
            for event_result in event_result_list:
                await self.event_channel.send(embed=await embS.get_embed_for_event_result(event_result))

    @timer_5_s.before_loop
    async def wait_for_bot(self):
        await dsS.bot.wait_until_ready()
        self.event_channel = await dsS.get_channel_by_id(town_events_channel)
