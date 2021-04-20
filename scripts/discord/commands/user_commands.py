import discord
from discord.ext import commands

from scripts.systems.high_level_systems.townManagingSystem import TownManagingSystem as tMS
from scripts.systems.low_level_systems.peopleSystem import PeopleSystem as pS
from scripts.systems.middle_level_systems.moneySystem import MoneySystem as mS
from scripts.systems.low_level_systems.statsSystem import StatsSystem as sS
from scripts.systems.high_level_systems.embedSystem import EmbedSystem as embS
from scripts.systems.utilities.close_enough_string_decoder import return_closest_string


class UserCommands(commands.Cog):

    """Category documentations"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def bank(self, ctx):
        embed = discord.Embed(title="Bank", description="Dostępne komendy", colour=discord.Colour(0x3e038c))
        embed.add_field(name="!przelewy", value="```Menu przelewów```", inline=True)
        embed.add_field(name="!wplaty", value="```Menu wpłat```", inline=True)
        embed.add_field(name="!inwestycje", value="```Menu inwestycji```", inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def przelewy(self, ctx):
        embed = discord.Embed(title="Menu Przelewów", colour=discord.Colour(0x3e038c))
        embed.add_field(name="Aby przelać komuś pieniądze:", value="Użyj `!przelej <kwota>` i oznacz użytkowników którym chcesz ją przelać", inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def wplaty(self, ctx):
        embed = discord.Embed(title="Menu Wpłat", colour=discord.Colour(0x3e038c))
        embed.add_field(name="Aby wpłacić pieniądze do banku:", value="Użyj `!wplac <kwota>`", inline=True)
        embed.add_field(name="Aby wypłacić pieniądze do banku:", value="Użyj `!wyplac <kwota>`", inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['obywatel', 'statistics'])
    async def stats(self, ctx):
        if ctx.message.mentions.__len__() > 0:
            tMS.actualize_user(ctx.message.mentions[0].id, ctx.message.mentions[0].nick, ctx.message.mentions[0].name)
            embed = embS.get_embed_for_stats(ctx.message.mentions[0])
        else:
            tMS.actualize_user(ctx.author.id, ctx.author.nick, ctx.author.name)
            embed = embS.get_embed_for_stats(ctx.author)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def travel(self, ctx, *args):
        if not tMS.check_if_user_travelling(ctx.author.id):
            current_location = sS.get_one(ctx.author.id).place
            list_of_places = tMS.get_possible_places_to_travel(current_location)
            if len(args) > 0:
                target_place_name = return_closest_string(args[0], [place.name for place in list_of_places])
                if target_place_name != '':
                    response, error = tMS.set_user_travelling(ctx.author.id, target_place_name, current_location)
                    await ctx.send(response)
                    return
                else:
                    await ctx.send("Nie ma takiej lokacji")
            else:
                embed = discord.Embed(title=f"Miejsca do których możesz się udać:", colour=discord.Colour(0x3e038c))
                places = tMS.get_possible_places_to_travel(sS.get_one(ctx.author.id).place)

                for place in places:
                    embed.add_field(name=place.name, value=f"```{tMS.get_travel_time_to_place(current_location, place.id)} minutes```", inline=True)
                await ctx.send(embed=embed)
        else:
            time_left = tMS.get_travel_time_left(ctx.author.id)
            await ctx.send(f"Właśnie podróżujesz do {tMS.get_destination_name(ctx.author.id)},"
                           f" dotrzesz za {time_left} sekund")

    @commands.command(pass_context=True)
    async def wplac(self, ctx, amount: int):
        response, error = tMS.insert_money_into_bank(ctx, amount)
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def wyplac(self, ctx, amount: int):
        response, error = tMS.payout_money_from_bank(ctx, amount)
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def miasteczko(self, ctx):
        embed = discord.Embed(title="Miasto", colour=discord.Colour(0x3e038c))
        embed.add_field(name="Ilość mieszkańców", value=f"```{pS.get_all().__len__()}```", inline=True)
        string_mieszkancy = ''
        for townie in pS.get_all():
            string_mieszkancy += townie.discord_nick + ', '
        embed.add_field(name="Mieszkańcy", value=f"```{string_mieszkancy}```", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def status(self, ctx, *args):
        if len(args) > 0:
            embed = embS.get_embed_for_statuses()
            await ctx.send('Nie możesz ustawiać statusów', embed=embed)
        else:
            embed = embS.get_embed_for_statuses()
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def stance(self, ctx, *args):
        if len(args) > 0:
            response, error = tMS.set_user_stance(ctx.author.id, int(args[0]))
            await ctx.send(response)
        else:
            embed = embS.get_embed_for_stances()
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def przelej(self, ctx, amount: int):
        response, error = tMS.transfer_money(ctx, ctx.message.mentions, amount)
        await ctx.send(response)

    @przelej.error
    async def przelej_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.BadArgument):
            await ctx.send("Kwota jest niepoprawna")

    @commands.command(pass_context=True)
    async def dodaj_plebsa(self, ctx):
        """Dodaje plebsa do miasta"""
        for emoji in ctx.message.guild.emojis:
            if emoji.name == 'PepoG':
                await ctx.message.add_reaction(emoji)
        for member in ctx.message.mentions:
            if pS.check_if_user_exist(member.id):
                await ctx.send(f'{member.nick} już jest obywatelem')
            else:
                tMS.create_user(member.id, member.nick)
                await member.send(f'Zostało Ci nadane obywatelstwo')

    @commands.command(pass_context=True, aliases=['hajs', 'portfel'])
    async def money(self, ctx):
        embed = discord.Embed(title=f"Stan konta {ctx.author.nick}:", colour=discord.Colour(0x3e038c))
        wallet = mS.get_wallet_from_user(ctx.author.id)
        if wallet is not False:
            embed.add_field(name=f"Hajs przy sobie:", value=f"```{wallet.cash_money}```", inline=False)
            embed.add_field(name=f"Hajs w banku:", value=f"```{wallet.bank_money}```", inline=False)
            await ctx.send(embed=embed)




