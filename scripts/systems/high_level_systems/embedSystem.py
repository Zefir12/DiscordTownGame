import discord
from scripts.systems.high_level_systems.townManagingSystem import TownManagingSystem as tMS
from scripts.systems.middle_level_systems.statusesSystem import StatusesSystem as stS
from scripts.systems.low_level_systems.peopleSystem import PeopleSystem as pS
from scripts.systems.middle_level_systems.stancesSystem import StancesSystem as stnS
from scripts.systems.middle_level_systems.travelSystem import TravelSystem as tS
from scripts.systems.middle_level_systems.eventSystem import EventResults
from scripts.discord.utilities.discord_bot_stuff import DiscordStuffSystem as dsS


class EmbedSystem:

    @staticmethod
    def get_embed_for_inventory():
        embed = discord.Embed(title="Inventory", colour=discord.Colour(0x3e038c))
        return embed

    @staticmethod
    def get_embed_for_statuses():
        statuses_list = tMS.get_possible_statuses()
        embed = discord.Embed(title="Statusy", colour=discord.Colour(0x3e038c))
        for status in statuses_list:
            embed.add_field(name=f"{status.id}: {status.name}", value=f"`{status.description}`", inline=True)
        return embed

    @staticmethod
    def get_embed_for_stances():
        stances_list = tMS.get_possible_stances()
        embed = discord.Embed(title="Stancje", colour=discord.Colour(0x3e038c))
        for stance in stances_list:
            embed.add_field(name=f"{stance.id}: {stance.name}", value=f"`{stance.description}`", inline=True)
        return embed

    @staticmethod
    def get_embed_for_stats(member):
        stats = tMS.get_user_stats(member.id)
        embed = discord.Embed(title=f"{member.nick}", colour=discord.Colour(0x3e038c))
        embed.set_thumbnail(url=member.avatar_url_as(size=128))
        embed.add_field(name=f"Level", value=f"```{stats.level}```", inline=True)
        embed.add_field(name=f"Experience", value=f"```{stats.experience}%```", inline=True)
        embed.add_field(name=f"Life Points", value=f"```[{stats.life_points}/{stats.max_life}]```", inline=True)
        embed.add_field(name=f"Status", value=f"```[{stS.get_one(stats.status).name}]```", inline=True)
        embed.add_field(name=f"Class", value=f"```{stats.character_class}```", inline=True)
        embed.add_field(name=f"Current Place", value=f"```{tS.get_one(stats.place).name}```", inline=True)
        if tMS.check_if_user_travelling(member.id):
            embed.add_field(name=f"Time Left", value=f"```{tMS.get_travel_time_left(member.id)}s```", inline=True)
        embed.add_field(name=f"Stance", value=f"```[{stnS.get_one(stats.stance).name}]```", inline=True)
        return embed

    @staticmethod
    async def get_embed_for_event_result(event_result: EventResults):
        embed = discord.Embed(title=f"{event_result.event_name}", colour=discord.Colour(0x3e038c))
        embed.add_field(name=f"User:", value=f"```{await dsS.get_user_name_by_id(event_result.user_id)}```", inline=True)
        embed.add_field(name=f"Event:", value=f"```{event_result.event_name}```", inline=True)
        embed.add_field(name=f"Items obtained:", value=f"```{event_result.get_received_item_as_string()}```", inline=True)
        return embed
