import discord
from discord.ext import commands
from scripts.managingRolesScript import RolesKOX



class ModeratorCommands(commands.Cog):

    """Category documentations"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['MegaModerator'], RolesKOX['Admin'])
    async def stworz_kategorie(self, ctx, nazwa_kategorii: str):
        """Sekretarz tworzy kategorie"""
        guild = ctx.guild
        await guild.create_category(str(nazwa_kategorii))
        await ctx.message.delete()
        for ch in guild.channels:
            if ch.name == nazwa_kategorii:
                await ch.create_text_channel('wykłady', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(689594911535923492): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('ćwiczenia-l1', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763120223251071037): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('ćwiczenia-l2', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763120322655420418): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('ćwiczenia-l3', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763120339654803476): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('laboratoria-l1', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763069916692873216): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('laboratoria-l2', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763069961777446942): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('laboratoria-l3', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763070010942816307): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('laboratoria-l4', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763070045374382080): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('laboratoria-l5', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763070030559707146): discord.PermissionOverwrite(read_messages=True)})
                await ch.create_text_channel('laboratoria-l6', overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_role(763070113002946601): discord.PermissionOverwrite(read_messages=True)})

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['MegaModerator'], RolesKOX['Admin'])
    async def add_emote(self, ctx, emoji_name, message_id: int):
        """Sekretarz emotkuje post z danym id"""
        message = await ctx.channel.fetch_message(message_id)
        for emoji in ctx.guild.emojis:
            print(emoji.name)
            if emoji.name == emoji_name:
                await message.add_reaction(emoji)
        await ctx.message.delete()

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['MegaModerator'], RolesKOX['Admin'])
    async def obsraj_post(self, ctx, message_id: int):
        emojiss = ['peppoHappy', 'Sadge', 'monkaW', 'monkaHmm', 'monkaCHRIST', 'HYPERS', 'monkaS', 'monkaGIGA']
        """Sekretarz sra emotami na post"""
        await ctx.message.delete()
        message = await ctx.channel.fetch_message(message_id)
        for emo in emojiss:
            for emoji in ctx.guild.emojis:
                if emoji.name == emo:
                    try:
                        await message.add_reaction(emoji)
                    except:
                        print(f'Już jest emotka {emo}')


    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['MegaModerator'], RolesKOX['Admin'])
    async def copy(self, ctx, msg_id):
        """Sekretarz repostuje tutaj post z danym id"""
        oryginal = await ctx.channel.fetch_message(msg_id)
        await ctx.channel.send(oryginal.content)
        await ctx.message.delete()

    @commands.command(pass_context=True)
    @commands.has_role('Moderator')
    async def sync_permissions(self, ctx, category_id: int):
        """Synchronizuje permisje z kategorią"""
        category = self.bot.get_channel(category_id)
        for channel in category.channels:
            if not channel.permissions_synced:
                await channel.edit(sync_permissions=True)
        await ctx.message.delete()

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['MegaModerator'], RolesKOX['Admin'])
    async def szukaj_channel(self, ctx, channel_id: int):
        """Podajesz id, zwraca nazwe kanału"""
        name = self.bot.get_channel(channel_id)
        await ctx.channel.send(name)
        await ctx.message.delete()

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['MegaModerator'], RolesKOX['Admin'])
    async def wyjeb_komendy(self, ctx, ilosc: int):
        """Czyśeci ostatnie 200 wiadomości zaczynających się !,$ lub -"""
        async for message in ctx.channel.history(limit=ilosc):
            if message.content.startswith('!') or message.content.startswith('$') or message.content.startswith('-'):
                await message.delete()

    @commands.command(pass_context=True)
    @commands.has_any_role(RolesKOX['MegaModerator'], RolesKOX['Admin'])
    async def wyjeb_wiadomosci_od_botow(self, ctx, ilosc: int):
        """Czyści dana liczbe wiadomosci od botów"""
        async for message in ctx.channel.history(limit=ilosc):
            if message.author.bot:
                await message.delete()
