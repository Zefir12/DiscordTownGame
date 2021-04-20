from scripts.systems.low_level_systems.peopleSystem import PeopleSystem as pS
from discord.ext.commands.context import Context


def check_if_person_in_database(ctx: Context) -> bool:
    return pS.check_if_user_exist(ctx.author.id)

