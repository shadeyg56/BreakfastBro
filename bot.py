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
    
bot = commands.Bot(command_prefix='b.')

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
    await bot.change_presence(game=discord.Game(name='Currently being coded'))
    
    
async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            # page = page.strip('```css').strip('```')


            await bot.send_message(ctx.message.channel, page)
        print('Sent command help')
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
        print('Sent command help')  


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
    user = ctx.message.author
    await bot.say('Got it. Headed to the kitchen now. Your order ID is {}'.format(id2))
    embed = discord.Embed(title='New Order, ID: {}'.format(id2), description=food, color=0xed)
    embed.set_author(name='{} | {}'.format(ctx.message.author, ctx.message.author.id), icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text='From: {} | {}'.format(ctx.message.server, ctx.message.server.id))
    await bot.send_message(kitchen, embed=embed)
    data = json.loads(open('ids.json').read())
    data[id2] = {}
    data = json.dumps(data, indent=4, sort_keys=True)
    with open('ids.json', 'w') as f:
         f.write(data)
    data = json.loads(open('ids.json').read())
    data[id2]["orderid"] = id2
    data[id2]["status"] = "unclaimed"
    data[id2]["user"] = user.id
    data[id2]["food"] = food
    data = json.dumps(data, indent=4, sort_keys=True)
    with open('ids.json', 'w') as f:
         f.write(data)
    bot.customer = ctx.message.author.id
    bot.food = '{}'.format(food)
    bot.channel = ctx.message.channel.id
    bot.id = id2
    bot.formatted = user
    bot.server = ctx.message.server

@bot.command(pass_context=True)
async def orders(ctx):
    with open('ids.json', 'r') as f:
        data = json.loads(f.read())
    await bot.say(data)
        
@bot.command(pass_context=True)
async def cook(ctx, orderid: str, pic_url: str):
    user = ctx.message.author
    bot.pic = '{}'.format(pic_url)
    delivery = bot.get_channel('366325049222889472')
    embed = discord.Embed(title='Pizza ready for delivery!, ID: {}'.format(orderid), description=bot.food, color = 0xed)
    embed.set_author(name='{} | {}'.format(bot.formatted, bot.customer), icon_url=bot.formatted.avatar_url)
    embed.set_footer(text='{} | {}'.format(bot.server, bot.server.id))
    with open('ids.json', 'r') as f:
        data = json.loads(f.read())
    if data[orderid]["orderid"] == '{}'.format(orderid):
        if data[orderid]["status"] == "claimed":
            if ctx.message.channel.id == '366325015488233493':
                x = data[orderid]["user"]
                x = '<@' + x + '>
                await bot.say('{0.mention}, cooking order {1}'.format(ctx.message.author, orderid))
                await bot.send_message(x, '{} has began cooking your order. This process takes about 3 minutes'.format(ctx.message.author))
                data[orderid]["pic_url"] = pic_url
                data[orderid]["status"] = "cooking"
                data = json.dumps(data, indent=4, sort_keys=True)
                with open('ids.json',  'w') as f:
                     f.write(data)
                await asyncio.sleep(180)
                with open('ids.json') as f:
                    data = json.loads(f.read())
                    data[orderid]["status"] = "cooked"
                await bot.send_message(delivery, embed=embed)
                await bot.send_message(x, 'Your order has finished cooking and should be delivered soon')
                data = json.dumps(data, indent=4, sort_keys=True)
                with open('ids.json', 'w') as f:
                    f.write(data)
    if not data[orderid] == '{}'.format(orderid):
        await bot.say('That order doesn\'t exist')
    
@bot.command(pass_context=True)
async def deliver(ctx, orderid: str):
    with open('ids.json', 'r') as f:
        data = json.loads(f.read())
    channel = bot.get_channel(bot.channel)
    formatted = '<@' +  + '>'
    if data[orderid]["orderid"] == '{}'.format(orderid):
        if data[orderid]["status"] == "cooked":
            if ctx.message.channel.id == '366325049222889472':
                x = data[orderid]["user"]
                x = '<@' + x + '>'
                food = data[orderid]["food"]
                await bot.say('{0.mention}, preparing your delivery'.format(ctx.message.author))
                await bot.send_message(x, '{} is now delivering your order. Your order will now be removed from the queue. Thanks for ordering from **Breakfast Bro**'.format(ctx.message.author))
                data[orderid]["orderid"] = "order_deleted"
                data[orderid]["status"] = 'order_deleted'
                url = data[orderid]['pic_url']
                await asyncio.sleep(5)
                invite = await bot.create_invite(channel)
                await bot.send_message(ctx.message.author, 'Here is your delivery for {}: **{}**.\nServer Invite: {}\nFood pic: {}'.format(x, food, invite, url))
    if not data[orderid]["orderid"] == '{}'.format(orderid):                                                               
        await bot.say('That order doesnt exist')
        
@bot.command(pass_context=True)
async def claim(ctx, orderid: str):
    with open('ids.json') as f:
        user = ctx.message.author
        data = json.loads(f.read())
    if data[orderid]["status"] == "unclaimed":
        if data[orderid]["orderid"] == '{}'.format(orderid):
            if ctx.message.channel.id == '366325015488233493':    
                data[orderid]["status"] = "claimed"
                x = data[orderid]['user']
                x = '<@' + x + '>'
                await bot.say('{0.mention}, You claimed order {1}'.format(ctx.message.author, orderid))
                await bot.send_message(x, '{} has claimed your order. They should start cooking it soon'.format(ctx.message.author))
        else:
             await bot.say("That order doesn\'t exist")
    else:
         await bot.say('That order has already been claimed')
    data = json.dumps(data, indent=4, sort_keys=True)
    with open('ids.json', 'w') as f:
        f.write(data)
            
            
@bot.command(pass_context=True)
async def invite(ctx):
    await bot.say('**Breakfast Bro Invite:** https://discordapp.com/oauth2/authorize?client_id=366768341026734080&scope=bot&permissions=66186303')
    
@bot.command(pass_context=True)
async def delorder(ctx, orderid: str, reason: str):
    with open('ids.json') as f:
        data = json.loads(f.read())
        food = data[orderid]["food"]
        customer = data[orderid]["user"]
        customer = '<@' + x + '>'
    if ctx.message.channel.id == '366325015488233493' or ctx.message.channel.id == '366325049222889472':
        if data[orderid]["orderid"] == '{}'.format(orderid):
            data[orderid]["orderid"] = "deleted"
            data[orderid]["status"] = "deleted"
            data[orderid]["reason"] = reason
            await bot.send_message(customer, 'Your order for {} has been deleted by {} because {}'.format(food, ctx.message.author, reason))
    if not data[orderid]["orderid"] == '{}'.format(orderid):
        await bot.say('That order doesn\'t exist')
    data = json.dumps(data, indent=4, sort_keys=True)
    with open('ids.json', 'w') as f:
        f.write(data)
        
    
                               
  

bot.run(TOKEN)
