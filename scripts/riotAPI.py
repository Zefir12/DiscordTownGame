from certs_and_tokens.TOKENS import riotAPI
import time
from riotwatcher import LolWatcher

milli_week = 604800000

watcher = LolWatcher(riotAPI)
my_region = 'eun1'

me = watcher.summoner.by_name(my_region, 'Master Aiden')
print(me)

my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
print(my_ranked_stats)

my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'], end_time=(int(time.time() * 1000) - (milli_week * 1)), begin_time=(int(time.time() * 1000) - (milli_week * 2)))



last_match = my_matches['matches'][0]
#match_detail = watcher.match.by_id(my_region, last_match['gameId'])
print(watcher.spectator.by_summoner(my_region, me['id']))


#latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
static_champ_list = watcher.data_dragon.champions("11.4.1", False, 'en_US')

