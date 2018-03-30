import discord
from discord.ext import commands
import private
import random
import json

bot = commands.Bot(command_prefix="b.", description="A food delivery bot created by shadeyg56 made for delivering virtual breakfast food to your server")
#temporary ids this is just for testing
ids = ["test", "test2"]


@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: shadeyg56')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    await bot.change_presence(activity=discord.Game(name="Being rewritten"))

@bot.command()
async def test(ctx):
	await ctx.send("I am alive")

@bot.command()
async def order(ctx, *, item:str):
	with open("orders.json") as f:
		orders = json.load(f)
	kitchen = bot.get_channel(366325015488233493)
	await ctx.send("Please make sure your order is a legitamate breakfast item, otherwise it will be automatically deleted. Reply yes to continue or no to cancel")
	x = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
	if x.content == "yes":
		id = random.choice(ids)
		await ctx.send(f"Your order has been sent to the kitchen where are expert ninja cooks will deal with it! Your order id is {id}!")
		embed = discord.Embed(title=f"New Order, ID: {id}", description=item)
		embed.set_author(name=f"{ctx.author} | {ctx.author.id}")
		embed.set_footer(text=f"From: {ctx.guild} | {ctx.guild.id}")
		await kitchen.send(embed=embed)
		if id in orders:
			pass
		else:
			orders[id] = {}
		orders[id] = item
		orders[id]["guild"] = ctx.guild.id
		orders[id]["status"] = "unclaimed"
		order[id]["customer"] = ctx.author.id
		orders = json.dumps(orders, indent=4)
		with open("orders.json", "w") as f:
			f.write(orders) 
	else:
		await ctx.send("Order Cancelled")

@bot.command()
async def claim(ctx, order_id: str):
	with open("orders.json") as f:
		orders = json.load(f)
	if order_id in orders:
		if orders[order_id]["status"] == "unclaimed":
			if ctx.channel.id == 366325015488233493:
				orders[order_id]["status"] = "claimed"
				orders[order_id]["chef"] = ctx.author.id
	else:
		await ctx.send('That order id doesn\'t exist.')



bot.run(private.TOKEN)