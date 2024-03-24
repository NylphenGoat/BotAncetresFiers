import discord
from discord.ext import commands
import random
from random import randint

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
users = {"name1" : "info",
         "name2" : "info",
         "name3" : "info",
         "name4" : "info",
         "name5" : "info",
         "name6" : "info"}



victoireDefaite = ['Victoire','Défaite']
colors = [discord.Colour.green(),discord.Colour.red()]

TOKEN = "your-bot-token"