import discord
from discord.ext import commands
import os

if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']
    
bot = commands.Bot(prefix='tbd')

@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: shadeyg56')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    
@bot.command(pass_context=True)
async def test(ctx):
    await bot.say('All systems operational')

bot.run(TOKEN)

