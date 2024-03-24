import discord
from discord.ext import commands,tasks
import random
from random import *
from variables import *
from riotwatcher import LolWatcher, ApiError
from lol import *
import asyncio
import requests
import json
import os

currend_directory = os.getcwd()

file_path = os.path.join(currend_directory,"messages.json")

os.chmod('messages.json', 0o666)

with open(file_path,'r',encoding='utf-8') as file:
    messages_data = json.load(file)
    defeat_messages = messages_data['defeat_messages']
    victory_messages = messages_data['victory_messages']


async def check_last_games():
    while True: # Endless loop of the function
        
        # Checking if the current last game of the user is the same as the last one registered,if not,then we register the new last game and we analyse it
        for el in RegisteredUsersList: 
            new_last_game = lol_watcher.match.matchlist_by_puuid(my_region,el['puuid'],0,1)[0]
            if new_last_game != LastgameUsers[el['name']]:
                LastgameUsers[el['name']] = new_last_game
                curGame = lol_watcher.match.by_id(my_region,LastgameUsers[el['name']])

                # Searching for the position of the current user in the array containing the 10 players of the game
                for i in range(10):
                    if curGame['info']['participants'][i]['summonerName'] == el['name']:
                        v = 2 #Variable used to decide which element of victoireDefaite and colors will be used for the embed

                        # Checking if the game was a win or not and then sending a message containing informations corresponding to the result of the game.
                        if not curGame['info']['participants'][i]['win']:
                            v = 1
                            if ((curGame['info']['participants'][i]['kills'] + curGame['info']['participants'][i]['assists'])/curGame['info']['participants'][i]['deaths'] < 1): #If the KDA of the player is < 1,then a special message is sent
                                ra = random.randint(0,1)
                                formatted_defeat_message = defeat_messages[ra].format(
                                summoner_name=curGame['info']['participants'][i]['summonerName'],
                                champion_name=curGame['info']['participants'][i]['championName'],
                                kills=curGame['info']['participants'][i]['kills'],
                                deaths=curGame['info']['participants'][i]['deaths'],
                                assists=curGame['info']['participants'][i]['assists'])
                                message = formatted_defeat_message
                            elif (curGame['info']['participants'][i]['summonerName'] == "summonner-name1" and (curGame['info']['participants'][i]['championName'] == "LeeSin" or curGame['info']['participants'][i]['championName'] == "Kayn")): #If summonner-name1 has lost a game on leeSin or Kayn(example),then a special message is sent
                                message = f"@everyone REGARDEZ MOI CETTE PERF ABOMINABLE DE SUMMONNER-NAME1 SUR SON LEGENDAIRE {curGame['info']['participants'][i]['championName']} !!LACHE CE CHAMPION !!! {curGame['info']['participants'][i]['deaths']} MORTS !!!"
                            else:
                                message =f"Nouvelle défaite de {curGame['info']['participants'][i]['summonerName']} sur {curGame['info']['participants'][i]['championName']} !"

                        else:
                            v = 0
                            if (curGame['info']['participants'][i]['kills'] >= 10 and curGame['info']['participants'][i]['deaths'] <= 3):
                                ra = random.randint(0,1)
                                formatted_victory_message = victory_messages[ra].format(
                                summoner_name=curGame['info']['participants'][i]['summonerName'],
                                champion_name=curGame['info']['participants'][i]['championName'],
                                kills=curGame['info']['participants'][i]['kills'],
                                deaths=curGame['info']['participants'][i]['deaths'],
                                assists=curGame['info']['participants'][i]['assists'])
                                message = formatted_victory_message
                            else:
                                message =f"Nouvelle victoire de {curGame['info']['participants'][i]['summonerName']} sur {curGame['info']['participants'][i]['championName']} !"
                        channel = bot.get_channel('your-channel-id')
                        channel_test = bot.get_channel('your-test-channel-id')
                        await channel_test.send(message) # Sending the selected message
                        gameIdTransformed = LastgameUsers[el['name']].replace("EUW1_","") # Removing the beginning part of the gameId to make it so that we only have the actual number
                        
                        #Creating an embed containing the link to the details of the game as well of the result and some important informations
                        embed_result = discord.Embed(
                            title = victoireDefaite[v],
                            description= f"Résultat du dernier match de {curGame['info']['participants'][i]['summonerName']} !",
                            colour = colors[v],
                            url = f'https://www.leagueofgraphs.com/match/euw/{gameIdTransformed}' #Using the transformed gameId to have a link directing to the match details
                        )
                        embed_result.add_field(name="Score",value = f"{curGame['info']['participants'][i]['kills']}/{curGame['info']['participants'][i]['deaths']}/{curGame['info']['participants'][i]['assists']}")
                        embed_result.add_field(name="Champion",value = f"{curGame['info']['participants'][i]['championName']}")
                        embed_result.add_field(name="Dégats aux champions",value = f"{curGame['info']['participants'][i]['totalDamageDealtToChampions']}")
                        await channel_test.send(embed = embed_result)

        await asyncio.sleep(10)

@tasks.loop(seconds = 10)
async def update_last_games():
    await check_last_games()

@bot.event
async def on_ready():
    channel_test = bot.get_channel(471318083785588738)
    await channel_test.send("Je suis prêt !")
    print("Nickel")
    update_last_games.start()



@bot.command()

async def infoUser(ctx : commands.Context,user : str) -> discord.Message:
    if user not in users:
        await ctx.send("Utilisateur non reconnu")
    first_embed = discord.Embed(
        title = user,
        description = users[user],
        color = discord.Color.red()
    )
    return await ctx.send(embed=first_embed)

@bot.command()
async def infoSummonner(ctx : commands.Context,name : str) -> discord.Message:
    print(name)
    sumonner = lol_watcher.summoner.by_name('euw1',name)
    sumonnerstats = lol_watcher.league.by_summoner(my_region,sumonner['id'])
    first_embed = discord.Embed(
        title = sumonnerstats[0]['summonerName'],
        description = f"Rang : {sumonnerstats[0]['tier']} {sumonnerstats[0]['rank']} {sumonnerstats[0]['leaguePoints']} lp",
        color = discord.Color.red()
    )
    return await ctx.send(embed=first_embed)





if __name__ == "__main__":
    bot.run(TOKEN)



