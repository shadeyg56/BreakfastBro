import discord
from discord.ext import commands
import os
import random

if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']
    
bot = commands.Bot(command_prefix='tbd')

id = ["gH1iT","jyRgE","TDq8s","jm2Q2","pbImA","OHKNp","Qov2Z","YW7jX","a4Oxt","vEK3t","iBwfM","s2tbO","zODd6","SyaLj","v2zAr","lh5un","VHwam","BRrla","UuQbt","KM7xv","5XtBL","V5rSC","K1eNh","rSU1q","4JKIa","a3o6b","PHPM5","7OXV1","OvaKB","yfN8M","PBEM1","jPqR2","VBTWo","8L0TE","KEDIM","AqbnA","mubnT","5KhwA","BDPL6","F1apM","6BOhM","3ZNSl","OGtpG","xi4JQ","62QLj","qFcB2","fBLGf","XjhYH","VSnQt","aSLx2","6hlSM","xa9ke","AGkPf","Lw4Gb","keg6Z","EwKeR","mePOU","X1thm","qdBRw","ml5X8","MspNi","xru7y","ljUqJ","dte33","w42nH","JMmBX","C8OOh","5hxSd","8flA7","By4x6","XAPNO","Aw1tc","QAwR2","o2Oh6","unN09","ZEOHN","4wA9p","Qv0zi","BuXBM","3w3fM","P9z3u","WbuY6","8z1do","H4Nn6","XRE08","28iFw","YQWcz","KN3Fc","F292c","aizlk","aTwWy","Vyzt5","f8w76","nRFsP","5b2YG","a3keE","8t9HJ","UYRf6","zByTY","NgPvP"]
@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: shadeyg56')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    await bot.change_presence(game=discord.Game(name='as Food Delivery testing. | Darkness not working atm'))
    
@bot.command(pass_context=True)
async def test(ctx):
    await bot.say('All systems operational')
    
@bot.command(pass_context=True)
async def order(ctx, *, food: str):
    num = random.randint(0, 100)
    await bot.say('Got it. Headed to the kitchen now. Your order ID is {}'.format(id[num]))

bot.run(TOKEN)
