from riotwatcher import LolWatcher, ApiError
import time

import variables

lol_watcher = LolWatcher('your-api-key')
my_region = 'euw1'#Your region
RegisteredUsersList = [lol_watcher.summoner.by_name(my_region,'summonner-name1'),lol_watcher.summoner.by_name(my_region,'summonner-name2'),lol_watcher.summoner.by_name(my_region,'summonner-name3'),lol_watcher.summoner.by_name(my_region,'summonner-name4'),lol_watcher.summoner.by_name(my_region,'summonner-name5')]
LastgameUsers = {} # Dictionnary that links a user and its last game

#For all registered users,adding their id and their last game in the dictionnary
for el in RegisteredUsersList:
    last_game = lol_watcher.match.matchlist_by_puuid(my_region,el['puuid'],0,1)
    LastgameUsers[el['name']] = last_game[0]
print(LastgameUsers)




