import pymongo


class TownDatabase:
    uri = "mongodb+srv://discordtowndb.zifbp.mongodb.net/<dbname>?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri, tls=True, tlsCertificateKeyFile='D:\Programowanie\Github Repositories\DiscordTownGame\certs_and_tokens\X509-cert-7952542027018750515.pem')
    database = client["DiscordTownDB"]
    test_database = client["test_database"]
    users = database["users"]
    town = database["town"]
    jobs = database["jobs"]
    money = database["money"]
    eq = database["eq"]
    stats = database["stats"]
    test = database["test"]
    test2 = database["test2"]
    static_data = database["static_data"]
    travel_connections = database["travel_connections"]
    places = database["places"]
    statuses_dict = database["statuses_dict"]
    stances_dict = database["stances_dict"]
    events = database["events"]
    items = database["items"]
    item_templates = database["item_templates"]
    item_pools = database["item_pools"]








