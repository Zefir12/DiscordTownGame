
class ChecksFunctionsClass:

    @staticmethod
    def enough_check(error, response, amount, minimum=0):
        if amount < minimum:
            return [True, f"Amount should be at least {minimum}"]
        return [error, response]

    @staticmethod
    def more_than_zero_check(error, response, amount):
        if amount <= 0:
            return [True, "Amount should be more than zero"]
        return [error, response]

    @staticmethod
    def list_not_empty_check(error, response, list_to_check):
        if len(list_to_check) == 0:
            return [True, "List shouldn't be empty"]
        return [error, response]

    @staticmethod
    def object_in_list_check(error, response, list_to_check, item):
        if item not in list_to_check:
            return [True, "Item is not in list"]
        return [error, response]