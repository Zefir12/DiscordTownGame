from scripts.systems.middle_level_systems.moneySystem import MoneySystem as mS
from scripts.systems.low_level_systems.peopleSystem import PeopleSystem as pS, TownUser
from scripts.systems.low_level_systems.statsSystem import StatsSystem as sS
from scripts.systems.middle_level_systems.travelSystem import TravelSystem as tS
from scripts.systems.middle_level_systems.inventorySystem import InventorySystem as iS
from scripts.systems.middle_level_systems.statusesSystem import StatusesSystem as stS
from scripts.systems.middle_level_systems.stancesSystem import StancesSystem as stanS
from scripts.systems.utilities.checks_functions import ChecksFunctionsClass as cFC


class TownManagingSystem:

    @staticmethod
    def create_user(id: int, name=None):
        if pS.create(id):
            if name is not None:
                pS.update_user(id, {'discord_nick': name})
            if sS.create(id):
                print('created stats')
            if iS.create(id):
                print('created inventory')
            pS.update_user(id, {'eq_id': id, 'stats_id': id})
            return mS.create_user_wallet(id)
        return False

    @staticmethod
    def actualize_user(_id, nick, name):
        pS.update_user(_id, {'discord_nick': nick, 'name': name})

    @staticmethod
    def delete_user(_id, belongings=True):
        if belongings:
            wallet = mS.get_wallet_from_user(_id)
            if wallet:
                mS.delete_wallet(wallet)
            else:
                print(f"Couldn't delete wallet with _id: {wallet.id}, of user: {_id}."
                      f" Either doesn't exists, or there is some other problem")
        return pS.delete_user(_id)

    @staticmethod
    def get_user_stats(_id):
        user: TownUser = pS.get_one(_id)
        if user is not False:
            if user.stats_id == -1:
                pS.update_user(_id, {'stats_id': _id})
                sS.create(_id)
                sS.change_owner(_id, _id)
            if sS.get_one(user.stats_id) is False:
                sS.create(_id)
                sS.change_owner(_id, _id)
            return sS.get_one(user.stats_id)
        return False

    @staticmethod
    def insert_money_into_bank(_id_or_ctx, amount: int):
        error, response = False, "None"
        if not isinstance(_id_or_ctx, int):
            _id_or_ctx = _id_or_ctx.author.id
        if amount <= 0:
            response = "Kwota mniejsza niż zero"
            error = True
        elif amount > mS.get_user_cash(_id_or_ctx):
            response = "Zbyt mało hajsu aby wpłacić"
            error = True
        if not error:
            mS.inc_money(_id_or_ctx, -amount, 'cash')
            mS.inc_money(_id_or_ctx, amount, 'bank')
            response = "Wpłata zakończona sukcesem"
        return [response, error]

    @staticmethod
    def payout_money_from_bank(_id_or_ctx, amount: int):
        error, response = False, "None"
        if not isinstance(_id_or_ctx, int):
            _id_or_ctx = _id_or_ctx.author.id
        if amount <= 0:
            response = "Kwota mniejsza niż zero"
            error = True
        elif amount > mS.get_user_money(_id_or_ctx):
            response = "Zbyt mało pieniędzy na koncie"
            error = True
        if not error:
            mS.inc_money(_id_or_ctx, -amount, 'bank')
            mS.inc_money(_id_or_ctx, amount, 'cash')
            response = "Wypłata zakończona sukcesem"
        return [response, error]

    @staticmethod
    def transfer_money(_id_or_ctx, list_of_members, amount: int):
        error, response = False, "None"
        if not isinstance(_id_or_ctx, int):
            _id_or_ctx = _id_or_ctx.author.id
        members_to_pay = [member for member in list_of_members if pS.check_if_user_exist(member.id) if member.id != _id_or_ctx]
        total_money_to_pay = len(members_to_pay) * amount
        error, response = cFC.more_than_zero_check(error, response, amount)
        error, response = cFC.list_not_empty_check(error, response, members_to_pay)
        error, response = cFC.enough_check(error, response, total_money_to_pay)
        if not error:
            [mS.transfer_money(_id_or_ctx, member, amount, 'bank') for member in members_to_pay]
            response = f"Wysłano w sumie {total_money_to_pay} do {[x.nick for x in members_to_pay]}"
        return [response, error]

    @classmethod
    def get_possible_places_to_travel(cls, current_location_id):
        """Returns list of travel connections"""
        travel_connections = tS.get_possible_travel_connections_to_travel(current_location_id)
        places_to_travel = []
        for travel_connection in travel_connections:
            if current_location_id == travel_connection['id1']:
                places_to_travel.append(tS.get_one(travel_connection['id2']))
            else:
                places_to_travel.append(tS.get_one(travel_connection['id1']))
        return places_to_travel

    @classmethod
    def get_travel_time_to_place(cls, current_place_id: int, target_place_id: int):
        """Returns travel time in minutes"""
        return tS.get_connection_between_places(current_place_id, target_place_id)['travel_time']

    @classmethod
    def set_user_travelling(cls, _id, destination_name, current_location_id):
        error, response = False, "None"
        destination_id = tS.get_one_by_query({'name': destination_name}).id

        connection = tS.get_connection_between_places(destination_id, current_location_id)
        time_of_travel = connection['travel_time']

        if time_of_travel is False:
            error = True
            response = "Wrong parameter as time of travel"

        if tS.check_if_user_travelling(_id):
            error = True
            response = "User is currently travelling already"

        error, response = cFC.object_in_list_check(error, response, [name.name for name in cls.get_possible_places_to_travel(current_location_id)], destination_name)
        if not error:
            sS.update_one_stat(_id, 'place', 0)
            sS.update_one_stat(_id, 'status', 4)
            tS.set_user_travelling(_id, tS.get_one_by_query({'name': destination_name}), time_of_travel)
            response = f"Wyruszyłeś do {destination_name}"
        return [response, error]

    @staticmethod
    def check_if_user_travelling(_id):
        return tS.check_if_user_travelling(_id)

    @staticmethod
    def get_destination_name(_id):
        return tS.get_one(pS.get_one(_id).travel_destination).name

    @staticmethod
    def get_travel_time_left(_id) -> int:
        return pS.get_one(_id).travel_time_left

    @staticmethod
    def inc_user_travel_time(_id, amount):
        tS.inc_user_travel_time(_id, amount)

    @staticmethod
    def get_users_currently_travelling():
        users = pS.get_many_by_query({'travel_time_left': {'$gt': 0}})
        users_travelling = []
        for user in users:
            if tS.check_if_user_travelling(user.id):
                users_travelling.append(user)
        return users_travelling

    @staticmethod
    def settle_finished_user_on_destination(_id):
        if not tS.check_if_user_travelling(_id):
            sS.update_stats(_id, {'place': pS.get_one(_id).travel_destination})
            sS.update_one_stat(_id, 'status', 1)
            tS.set_user_finished_travelling(_id)
            return True
        return False

    @staticmethod
    def set_user_status(_id: int, status_id: int):
        error, response = False, "None"
        status = stS.get_one(status_id)
        if status is not False:
            if sS.update_one_stat(_id, 'status', status.id):
                response = "Pomyślnie ustawiono status"
                return [response, error]
        return ["Couldn't update status", True]

    @staticmethod
    def set_user_stance(_id: int, stance_id: int):
        error, response = False, "None"
        stance = stanS.get_one(stance_id)
        if stance is not False:
            if sS.update_one_stat(_id, 'stance', stance.id):
                response = "Pomyślnie ustawiono stancję"
                return [response, error]
        return ["Couldn't update stance", True]

    @staticmethod
    def get_possible_statuses():
        return stS.get_all()

    @staticmethod
    def get_possible_stances():
        return stanS.get_all()

    @staticmethod
    def _actualize_all_users():
        users = pS.get_all()
        for user in users:
            user.eq_id = user.id
            user.stats_id = user.id
            pS.update_user(user.id, user.json())
            sS.create(user.id)
            iS.create(user.id)

