from scripts.systems.low_level_systems.peopleSystem import dM, tD, PeopleSystem as pS, TownUser
from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass
from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF


class Wallet(BaseDatabaseClass):
    def __init__(self, _id):
        self._id = _id
        self.id = _id
        self.owner_id = -1
        self.cash_money = 0
        self.bank_money = 0


class MoneySystem(uF):
    _class_template = Wallet
    _collection = tD.money

    @staticmethod
    def delete_wallet(_id_or_wallet):
        """Returns true if successfully deleted, False otherwise.
        As arguments pass {_id}[int] or {wallet}[Wallet object]"""
        if isinstance(_id_or_wallet, int):
            return dM.delete_one(tD.money, {'_id': _id_or_wallet})
        elif isinstance(_id_or_wallet, Wallet):
            return dM.delete_one(tD.money, {'_id': _id_or_wallet.id})
        else:
            return False

    @classmethod
    def get_wallet_from_user(cls, _id_or_user):
        """Returns single Wallet object, False if something went wrong"""
        if isinstance(_id_or_user, TownUser):
            return cls.get_one(_id_or_user.wallet_id)
        elif isinstance(_id_or_user, int):
            user = pS.get_one(_id_or_user)
            if user:
                return cls.get_one(user.wallet_id)
            return False
        else:
            return False

    @staticmethod
    def connect_wallet_to_user_by_id(user_id: int, wallet_id: int):
        """Returns True if connected successfully, False otherwise"""
        # in work
        if dM.update_one(tD.money, {"_id": wallet_id}, {'owner_id': user_id}):
            return pS.update_user(user_id, {'wallet_id': wallet_id})
        return False

    @classmethod
    def create_user_wallet(cls, _id_or_user):
        """Returns True if created successfully, False otherwise"""
        if isinstance(_id_or_user, int):
            if cls.create(_id_or_user):
                return cls.connect_wallet_to_user_by_id(_id_or_user, _id_or_user)
            return False
        elif isinstance(_id_or_user, TownUser):
            if cls.create(_id_or_user.id):
                return cls.connect_wallet_to_user_by_id(_id_or_user.id, _id_or_user.id)
            return False

    # Increase Money section

    @classmethod
    def inc_money_by_wallet(cls, _id_or_wallet, amount: float, money_type: str):
        """Returns True if successful, False otherwise"""
        if isinstance(_id_or_wallet, int):
            wallet = cls.get_one(_id_or_wallet)
            if wallet:
                return dM.increment_one(tD.money, {'_id': _id_or_wallet}, {f'{money_type}_money': amount})
            return False
        elif isinstance(_id_or_wallet, Wallet):
            wallet = cls.get_one(_id_or_wallet.id)
            if wallet:
                return dM.increment_one(tD.money, {'_id': _id_or_wallet.id}, {f'{money_type}_money': amount})
            return False
        else:
            return False

    @classmethod
    def inc_money(cls, _id_or_user, amount: float, money_type: str):
        """Returns True if successful, False otherwise.
        User should be either {_id}[int] or {user}[TownUser object]"""
        if isinstance(_id_or_user, TownUser):
            wallet = cls.get_wallet_from_user(_id_or_user.id)
            if wallet:
                return cls.inc_money_by_wallet(wallet.id, amount, money_type)
            return False
        elif isinstance(_id_or_user, int):
            wallet = cls.get_wallet_from_user(_id_or_user)
            if wallet:
                return cls.inc_money_by_wallet(wallet.id, amount, money_type)
            return False
        else:
            return False

    # Transferring money section

    @classmethod
    def transfer_money_by_wallet_ids(cls, sender_wallet, receiver_wallet, amount: float, money_type: str):
        """Returns True if successful, False otherwise"""
        if cls.wallet_money(sender_wallet) < amount:
            return False
        return cls.inc_money_by_wallet(receiver_wallet, amount, money_type)

    @classmethod
    def transfer_money(cls, sender_id_or_user, receiver_id_or_user, amount: float, money_type: str):
        """Returns True if successful, False otherwise"""
        if cls.get_user_money(sender_id_or_user) < amount:
            return False
        if cls.inc_money(sender_id_or_user, -amount, money_type):
            return cls.inc_money(receiver_id_or_user, amount, money_type)
        return False

    # Getting money section

    @classmethod
    def get_user_money(cls, _id_or_user):
        """Returns amount[float] if successful, False otherwise"""
        if isinstance(_id_or_user, int):
            user = pS.get_one(_id_or_user)
            if user:
                wallet: Wallet
                wallet = cls.get_wallet_from_user(user)
                if wallet:
                    return wallet.bank_money
            return False
        elif isinstance(_id_or_user, TownUser):
            wallet = cls.get_wallet_from_user(_id_or_user)
            if wallet:
                return wallet.bank_money
            return False
        else:
            return False

    @classmethod
    def get_user_cash(cls, _id_or_user):
        """Returns amount[float] if successful, False otherwise"""
        if isinstance(_id_or_user, int):
            user = pS.get_one(_id_or_user)
            if user:
                wallet = cls.get_wallet_from_user(user)
                if wallet:
                    return wallet.cash_money
            return False
        elif isinstance(_id_or_user, TownUser):
            wallet = cls.get_wallet_from_user(_id_or_user)
            if wallet:
                return wallet.cash_money
            return False
        else:
            return False

    @staticmethod
    def wallet_money(_id_or_wallet):
        """Returns amount[float] or False if something went wrong"""
        if isinstance(_id_or_wallet, int):
            return dM.get_one(tD.money, {'_id': _id_or_wallet})['bank_money']
        elif isinstance(_id_or_wallet, Wallet):
            return _id_or_wallet.bank_money
