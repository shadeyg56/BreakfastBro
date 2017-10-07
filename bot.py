import discord
from discord.ext import commands

if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']
    
bot = commands.Bot(prefix='tbd')

bot.run(TOKEN)

