import discord
from discord.ext import commands
import os
import random
import json
from tinydb import TinyDB, Query
import asyncio
from tinydb.operations import delete

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
    
@bot.event
async def on_command_error(error, ctx):
   print(error)
   channel = ctx.message.channel
   if isinstance(error, commands.MissingRequiredArgument):
       await send_cmd_help(ctx)
       print('Sent command help')
   elif isinstance(error, commands.BadArgument):
       await send_cmd_help(ctx)
       print('Sent command help')
   elif isinstance(error, commands.DisabledCommand):
       await bot.send_message(channel, "That command is disabled.")
       print('Command disabled.')
   elif isinstance(error, commands.CommandInvokeError):
       # A bit hacky, couldn't find a better way
       no_dms = "Cannot send messages to this user"
       is_help_cmd = ctx.command.qualified_name == "help"
       is_forbidden = isinstance(error.original, discord.Forbidden)
       if is_help_cmd and is_forbidden and error.original.text == no_dms:
           msg = ("I couldn't send the help message to you in DM. Either you blocked me or you disabled DMs in this server.")
           await bot.send_message(channel, msg)
           return    
    
@bot.command(pass_context=True)
async def test(ctx):
    await bot.say('All systems operational')
    
@bot.command(pass_context=True)
async def order(ctx, *, food: str):
    num = random.randint(0, 100)
    kitchen = bot.get_channel('366325015488233493')
    id2 = id[num]
    bot.customer = ctx.message.author.id
    await bot.say('Got it. Headed to the kitchen now. Your order ID is {}'.format(id2))
    embed = discord.Embed(title='New Order, ID: {}'.format(id2), description=food, color=0xed)
    embed.set_author(name='{} | {}'.format(ctx.message.author, ctx.message.author.id), icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text='From: {} | {}'.format(ctx.message.server, ctx.message.server.id))
    await bot.send_message(kitchen, embed=embed)
    with open('ids.json') as f:
        data = json.loads(f.read())
        data[ctx.message.author] = bot.customer
        data['order_id'] = id2
        data = json.dumps(data, indent=4, sort_keys=True)
    with open('ids.json', 'w') as f:
        f.write(data)
    bot.customer = ctx.message.author.id
    bot.food = '{}'.format(food)

@bot.command(pass_context=True)
async def orders(ctx):
    with open('ids.json', 'r') as f:
        data = json.loads(f.read())
        await bot.say(data)
        
@bot.command(pass_context=True)
async def cook(ctx, orderid: str, pic_url: str = None):
    user = ctx.message.author
    delivery = bot.get_channel('366325049222889472')
    embed = discord.Embed(title='Pizza ready for delivery!, ID: {}'.format(orderid), description=bot.food, color = 0xed)
    embed.set_author(name='{} | {}'.format(user, user.id), icon_url=user.avatar_url)
    embed.set_footer(text='{} | {}'.format(ctx.message.server, ctx.message.server.id))
    with open('ids.json', 'r') as f:
        data = json.loads(f.read())
    if '{}'.format(orderid) in data.values():
        await bot.say('{0.mention}, cooking order {1}'.format(ctx.message.author, orderid))
        await asyncio.sleep(5)
        await bot.send_message(delivery, embed=embed)
    if not '{}'.format(orderid) in data.values():
        await bot.say('That order doesn\'t exist')
        
@bot.event
async def on_message(message):
    if message.content.startswith('d.'):
        await bot.send_message(message.channel, 'Sorry, but Darkness isn\'t available for use right now. It is currently being used for testing and should be up soon. Sorry for the inconvience. -Shadeyyy, Darkness Dev')
    await bot.process_commands(message)
    
@bot.command(pass_context=True)
async def deliver(ctx, orderid: str):
    with open('ids.json', 'r') as f:
        data = json.loads(f.read())
        data[bot.customer]
        x = f'{data[bot.customer]}'
    if '{}'.format(orderid) in data.values():
        await bot.say(x)
        await bot.say('{0.mention}, preparing your delivery'.format(ctx.message.author))
        await asyncio.sleep(5)
        await bot.send_message(ctx.message.author, 'Here is your delivery for null: **null**.\nServer Invite: null')
    if not '{}'.format(orderid) in data.values():                                                               
        await bot.say('That order doesnt exist')
                               
  

bot.run(TOKEN)
