from scripts.database.onlineMongoDB import TownDatabase


def check_connection():
    try:
        TownDatabase.client.server_info()
        return True
    except:
        return False

