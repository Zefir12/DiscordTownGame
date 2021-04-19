Roles = {
    '@everyone': 689594730807558147,
    'L06': 763070113002946601,
    'L05': 763070030559707146,
    'L04': 763070045374382080,
    'L03': 763070010942816307,
    'L02': 763069961777446942,
    'L01': 763069916692873216,
    'Elektrotechnik': 689594911535923492,
    'Edytor': 689841850659766314,
    'Moderator': 689595031698407461,
    'Sołtys': 689880572142944275,
    'Bot': 763073551438708756,
    'Ćw1': 763120223251071037,
    'Ćw2': 763120322655420418,
    'Ćw3': 763120339654803476,
    'Archiwum': 763131505014341633
    }

RolesKOX = {
    'MegaModerator': 'Minister',
    'Admin': 'Bot',
    'Moderator': 'Ministrant',
    }


def check_if_it_is_me(ctx):
    return ctx.message.author.id == 289041036364480512


def manage_roles(give, payload, bott):
    if give:
        guild = bott.get_guild(payload.guild_id)

        if payload.emoji.name == 'l1':
            role = guild.get_role(Roles["L01"])
            message = 'Zostałeś przydzielony do grupy L01'
        elif payload.emoji.name == 'l2':
            role = guild.get_role(Roles["L02"])
            message = 'Zostałeś przydzielony do grupy L02'
        elif payload.emoji.name == 'l3':
            role = guild.get_role(Roles["L03"])
            message = 'Zostałeś przydzielony do grupy L03'
        elif payload.emoji.name == 'l4':
            role = guild.get_role(Roles["L04"])
            message = 'Zostałeś przydzielony do grupy L04'
        elif payload.emoji.name == 'l5':
            role = guild.get_role(Roles["L05"])
            message = 'Zostałeś przydzielony do grupy L05'
        elif payload.emoji.name == 'l6':
            role = guild.get_role(Roles["L06"])
            message = 'Zostałeś przydzielony do grupy L06'
        elif payload.emoji.name == 'c1':
            role = guild.get_role(Roles["Ćw1"])
            message = 'Zostałeś przydzielony do grupy ćwiczeniowej: Ćw1'
        elif payload.emoji.name == 'c2':
            role = guild.get_role(Roles["Ćw2"])
            message = 'Zostałeś przydzielony do grupy ćwiczeniowej: Ćw2'
        elif payload.emoji.name == 'c3':
            role = guild.get_role(Roles["Ćw3"])
            message = 'Zostałeś przydzielony do grupy ćwiczeniowej: Ćw3'
        else:
            return False, False
    else:
        guild = bott.get_guild(payload.guild_id)

        if payload.emoji.name == 'l1':
            role = guild.get_role(Roles["L01"])
            message = 'Zabrałem ci rolę: L01'
        elif payload.emoji.name == 'l2':
            role = guild.get_role(Roles["L02"])
            message = 'Zabrałem ci rolę: L02'
        elif payload.emoji.name == 'l3':
            role = guild.get_role(Roles["L03"])
            message = 'Zabrałem ci rolę: L03'
        elif payload.emoji.name == 'l4':
            role = guild.get_role(Roles["L04"])
            message = 'Zabrałem ci rolę: L04'
        elif payload.emoji.name == 'l5':
            role = guild.get_role(Roles["L05"])
            message = 'Zabrałem ci rolę: L05'
        elif payload.emoji.name == 'l6':
            role = guild.get_role(Roles["L06"])
            message = 'Zabrałem ci rolę: L06'
        elif payload.emoji.name == 'c1':
            role = guild.get_role(Roles["Ćw1"])
            message = 'Zabrałem ci rolę: Ćw1'
        elif payload.emoji.name == 'c2':
            role = guild.get_role(Roles["Ćw2"])
            message = 'Zabrałem ci rolę: Ćw2'
        elif payload.emoji.name == 'c3':
            role = guild.get_role(Roles["Ćw3"])
            message = 'Zabrałem ci rolę: Ćw3'
        else:
            return False, False

    print(role, message)
    return role, message
