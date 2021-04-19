from scripts.systems.low_level_systems.databaseManager import DatabaseManager as tDM
from onlineMongoDB import TownDatabase as tD
from scripts.systems.middle_level_systems.peopleSystem import PeopleSystem as pS
import random
import time


def round_to_milis(number):
    return round(number * 10000) / 10000


def results(typee, check, time_before):
    if check:
        print(f'Test: [{typee}]{" " * (20 - typee.__len__())} passed successfully, and took: {round_to_milis(time.time() - time_before)} seconds')
    else:
        print(f'Test: [{typee}] failed!')
    return time.time()


def header_text(name):
    print("\n=========================")
    print(name)
    print("=========================\n")


def tdm_test():
    header_text('TownDatabaseManager Tests')
    """First deleting the collection(for safety of test) and creating test data"""
    tD.test.drop()
    test_data0 = random.randint(1, 100)
    random_array = []
    random_length = random.randint(10, 190)
    for b in range(random_length):
        random_array.append({'_id': b, 'data': random.randint(1, 100)})

    """By inserting we create collection"""
    start_time = time.time()

    """Testing Getting"""

    get_one = results('get_one', tDM.get_one(tD.static_data, {"_id": 0})['value'] == 173536, start_time)

    get_many = results('get_many', tDM.get_many(tD.static_data, {'type': 'test_data'}).__len__() == 2, get_one)

    get_all = results('get_all', tDM.get_all(tD.static_data).__len__() == 2, get_many)

    """Testing Inserting"""

    tDM.insert_one(tD.test, {"_id": -1, "data": test_data0})
    insert_one = results('insert_one', tDM.get_one(tD.test, {'_id': -1})['data'] == test_data0, get_all)

    tDM.insert_many(tD.test, random_array)
    test_many_check = True
    many_data = tDM.get_many(tD.test, {'_id': {'$ne': -1}})
    for data in many_data:
        if data not in random_array:
            test_many_check = False
    if many_data.__len__() != random_length:
        test_many_check = False
    insert_many = results('insert_many', test_many_check, insert_one)

    """Testing Incrementing"""

    tDM.increment_one(tD.test, {'_id': -1}, {'data': 1})
    increment_one = results('increment_one', tDM.get_one(tD.test, {'_id': -1})['data'] == test_data0 + 1, insert_many)

    tDM.increment_many(tD.test, {'_id': {'$ne': -1}}, {'data': 1})
    test_inc_many_check = True
    many_data = tDM.get_many(tD.test, {'_id': {'$ne': -1}})
    for data in many_data:
        if data['data'] - 1 != random_array[data['_id']]['data']:
            test_inc_many_check = False
    increment_many = results('increment_many', test_inc_many_check, increment_one)

    tDM.increment_all(tD.test, {'data': -1})
    test_inc_all_check = True
    many_data = tDM.get_many(tD.test, {'_id': {'$ne': -1}})
    for data in many_data:
        if data not in random_array:
            test_inc_all_check = False
    increment_all = results('increment_all', test_inc_all_check, increment_many)

    """Testing Updating"""

    tDM.update_one(tD.test, {'_id': -1}, {'data': 0})
    update_one = results('update_one', tDM.get_one(tD.test, {'_id': -1})['data'] == 0, increment_all)

    tDM.update_many(tD.test, {'_id': {'$ne': -1}}, {'data': 0})
    test_upd_many_check = True
    many_data = tDM.get_many(tD.test, {'_id': {'$ne': -1}})
    for data in many_data:
        if data['data'] != 0:
            test_upd_many_check = False
    update_many = results('update_many', test_upd_many_check, update_one)

    tDM.update_all(tD.test, {'data': 121})
    test_upd_all_check = True
    many_data = tDM.get_all(tD.test)
    for data in many_data:
        if data['data'] != 121:
            test_upd_all_check = False
    update_all = results('update_all', test_upd_all_check, update_many)

    """Testing Deleting"""

    tDM.delete_one(tD.test, {'_id': -1})
    delete_one = results('delete_one', tDM.get_all(tD.test).__len__() == random_length, update_all)

    tDM.delete_many(tD.test, {'_id': {'$not': {'$in': [0, 1]}}})
    delete_many = results('delete_many', tDM.get_all(tD.test).__len__() == 2, delete_one)

    tDM.delete_all(tD.test)
    delete_all = results('delete_all', not tDM.get_all(tD.test), delete_many)


def ps_test():
    header_text('PeopleSystem Tests')
    start_time = time.time()

    """Testing Inserting"""
    pS.create(600)
    insert_new_user = results('insert_new_user', pS.get_one(600).id == 600, start_time)

    pS.check_if_user_exist(600)
    check_if_user_exist = results('check_if_user_exist', pS.check_if_user_exist(600), insert_new_user)

    pS.delete_user(600)
    delete_user = results('delete_user', not pS.get_one(600), check_if_user_exist)


tdm_test()
ps_test()
