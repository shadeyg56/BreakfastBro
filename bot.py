import discord
from discord.ext import commands
import private
import random
import json
import asyncio

bot = commands.Bot(command_prefix=commands.when_mentioned_or("b."), description="A food delivery bot created by shadeyg56 made for delivering virtual breakfast food to your server")
Alphabet = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z"]



@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: shadeyg56')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    await bot.change_presence(activity=discord.Game(name="Huge Rewrite | b.help | b.order"))

@bot.event
async def on_command_error(ctx, error):
	print(error)
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'`Usage: {ctx.prefix + ctx.command.signature}`')
		print('Sent command help')
	#elif isinstance(error, send_help):
		#print('Sent command help')
	elif isinstance(error, commands.DisabledCommand):
		await ctx.send("That command is disabled.")
		print('Command disabled.')
	elif isinstance(error, commands.NotOwner):
		await ctx.send("You're not a developer silly")
		print("Attemepted dev command by non-dev")

@bot.command()
async def test(ctx):
	await ctx.send("I am alive")

@bot.command()
async def order(ctx, *, item:str):
	with open("data/orders.json") as f:
		orders = json.load(f)
	kitchen = bot.get_channel(366325015488233493)
	await ctx.send("Please make sure your order is a legitamate breakfast item, otherwise it will be automatically deleted. Reply yes to continue or no to cancel")
	x = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
	if x.content == "yes":
		id = random.choice(Alphabet) + random.choice(Alphabet) + random.choice(Alphabet) + random.choice(Alphabet) + random.choice(Alphabet) + random.choice(Alphabet)
		await ctx.send(f"Your order has been sent to the kitchen where are expert ninja cooks will deal with it! Your order id is {id}!")
		embed = discord.Embed(title=f"New Order, ID: {id}", description=item)
		embed.set_author(name=f"{ctx.author} | {ctx.author.id}")
		embed.set_footer(text=f"From: {ctx.guild} | {ctx.guild.id}")
		await kitchen.send(embed=embed)
		if id in orders:
			pass
		else:
			orders[id] = {}
		orders[id]["item"] = item
		orders[id]["guild"] = str(ctx.guild.id)
		orders[id]["status"] = "unclaimed"
		orders[id]["customer"] = str(ctx.author.id)
		orders = json.dumps(orders, indent=4)
		with open("data/orders.json", "w") as f:
			f.write(orders) 
	else:
		await ctx.send("Order Cancelled")

@bot.command()
async def claim(ctx, order_id: str):
	with open("data/orders.json") as f:
		orders = json.load(f)
	with open("data/workers.json") as f:
		workers = json.load(f)
	if order_id in orders:
		if orders[order_id]["status"] == "unclaimed":
			if str(ctx.author.id) in workers["workers"]:
				if "chef" in workers["workers"][str(ctx.author.id)]["jobs"]: 
					orders[order_id]["status"] = "claimed"
					orders[order_id]["chef"] = str(ctx.author.id)
					await ctx.send(f"{ctx.author.mention}, you claimed order {order_id}")
					orders = json.dumps(orders, indent=4)
					with open("data/orders.json", "w") as f:
						f.write(orders)
		else:
			await ctx.send("That order is already claimed or being cooked/is cooked or needs to be delivered")
	else:
		await ctx.send('That order id doesn\'t exist.')

@bot.command()
async def orders(ctx):
	with open("data/orders.json") as f:
		orders = json.load(f)
	with open("data/workers.json") as f:
		workers = json.load(f)
	if str(ctx.author.id) in workers["workers"]:
		embed = discord.Embed(title="Current Orders", color=discord.Color.blue())
		unclaimed = []
		claimed = []
		cooking = []
		cooked = []
		for ids in orders:
			if orders[ids]["status"] == "unclaimed":
				list(unclaimed)
				unclaimed.append(ids)
		
			if orders[ids]["status"] == "claimed":
				list(claimed)
				claimed.append(ids)
			
			if orders[ids]["status"] == "cooking":
				list(cooking)
				cooking.append(ids)
		
			if orders[ids]["status"] == "cooked":
				list(cooked)
				cooked.append(ids)
			
		if len(unclaimed) == 0:
			unclaimed = "None"
		if len(claimed) == 0:
			claimed  = "None"
		if len(cooking) == 0:
			cooking = "None"
		if len(cooked) == 0:
			cooked = "None"
		if unclaimed != "None":
			unclaimed = ", ".join(unclaimed)
		if claimed != "None":
			claimed = ", ".join(claimed)
		if cooking != "None":
			cooking = ", ".join(cooking)
		if cooked != "None":
			cooked = ", ".join(cooked)
		embed.add_field(name="Unclaimed", value=unclaimed)
		embed.add_field(name="Claimed", value=claimed)
		embed.add_field(name="Cooking", value=cooking)
		embed.add_field(name="Cooked", value=cooked)
		await ctx.send(embed=embed)

@bot.command()
async def cook(ctx, order_id, pic_url:str = None):
	delivery = bot.get_channel(366325049222889472)
	with open("data/orders.json") as f:
		orders = json.load(f)
	with open("data/workers.json") as f:
		workers = json.load(f)
	customer = orders[order_id]["customer"]
	guild = orders[order_id]["guild"]
	customer = bot.get_user(int(customer))
	guild = bot.get_guild(int(guild))
	if order_id in orders:
		if orders[order_id]["status"] == "claimed":
			if str(ctx.author.id) in workers["workers"]:
				if "chef" in workers["workers"][str(ctx.author.id)]["jobs"]:
					if str(ctx.author.id) == orders[order_id]["chef"]:
						orders[order_id]["status"] = "cooking"
						orders = json.dumps(orders, indent=4)
						with open("data/orders.json", "w") as f:
							f.write(orders)
						with open("data/orders.json") as f:
							orders = json.load(f)
						if pic_url:
							orders[order_id]["pic_url"] = pic_url
						else:
							orders[order_id]["pic_url"] = "None"
						await ctx.send(f"Cooking order {order_id}")
						await customer.send(f"{ctx.author} is now cooking your order. This process takes about 3 min")
						await asyncio.sleep(10)
						embed = discord.Embed(title=f"Order ready for delivery, ID: {order_id}", description=orders[order_id]["item"], color=discord.Color.blue())
						orders[order_id]["status"] = "cooked"
						embed.set_author(name=f"{customer.name} | {customer.id}", icon_url=customer.avatar_url)
						embed.set_footer(text=f"{guild.name} | {guild.id}")
						await delivery.send(embed=embed)
						await customer.send("Your order has finsihed cooking and is ready to be delivered. Be on the lookout.")
						orders = json.dumps(orders, indent=4)
						with open("data/orders.json", "w") as f:
							f.write(orders)
					else:
						x = bot.get_user(int(orders[order_id]["chef"]))
						await ctx.send(f"{x.name} already claimed this order")
				else:
					await ctx.send("You're not a chef")
	else:
		await ctx.send("That order doesn't exist")

@bot.command()
async def deliver(ctx, order_id):
	with open("data/orders.json") as f:
		orders = json.load(f)
	with open("data/workers.json") as f:
		workers = json.load(f)
	customer = orders[order_id]["customer"]
	guild = orders[order_id]["guild"]
	customer = bot.get_user(int(customer))
	guild = bot.get_guild(int(guild))
	if order_id in orders:
		if orders[order_id]["status"] == "cooked":
			if str(ctx.author.id) in workers["workers"]:
				if "delivery" in workers["workers"][str(ctx.author.id)]["jobs"]:
					await ctx.send(f"{ctx.author.mention}, preparing your delivery")
					await customer.send(f"{ctx.author.name} is now delivering your order. Your order will now be removed from the queue. Thanks for ordering from **Breakfast Bro**")
					await asyncio.sleep(5)
					invite = await guild.channels[0].create_invite(reason="Created for delivering a customer's food")
					await ctx.author.send(f"Here is your delivery for {customer.name}: **{orders[order_id]['item']}**.\nServer Invite: {invite}\nFood pic: {orders[order_id]['pic_url']}")
					del orders[order_id]
					data = json.dumps(orders, indent=4)
					with open("data/orders.json", "w") as f:
						f.write(data)
	else:			
		await ctx.send("That order doesn't exist")

@bot.command()
async def delorder(ctx, order_id, *, reason: str):
	with open("data/orders.json") as f:
		orders = json.load(f)
	with open("data/workers.json") as f:
		workers = json.load(f)
	customer = orders[order_id]["customer"]
	guild = orders[order_id]["guild"]
	customer = bot.get_user(int(customer))
	guild = bot.get_guild(int(guild))
	if order_id in orders:
		if str(ctx.author.id) in workers["workers"]:
			await ctx.send(f"Order {order_id} succesfully deleted")
			await customer.send(f"Your order for {orders[order_id]['item']} has been deleted by {ctx.author.name} because {reason}")
			del orders[order_id]
			data = json.dumps(orders, indent=4)
			with open("data/orders.json", "w") as f:
						f.write(data)
						if orders == "":
							f.write("{}")
	else:
		await ctx.send("That order doesn't exist")

@bot.command()
async def add_worker(ctx, user: discord.Member, job):
	jobs = ["chef", "delivery"]
	with open("data/workers.json") as f:
		workers = json.load(f)
	if str(ctx.author.id) in workers["workers"]:
		if "management" in workers["workers"][str(ctx.author.id)]["jobs"]:
			if job in jobs:
				await ctx.send(f"Added {user.mention} to the {job.title()} job")
				if str(user.id) not in workers["workers"]:
					workers["workers"][str(user.id)] = {}
					workers["workers"][str(user.id)]["name"] = user.name
					workers["workers"][str(user.id)]["jobs"] = {}
					workers["workers"][str(user.id)]["jobs"][job] = {}
				else:
					workers["workers"][str(user.id)]["jobs"][job] = {}
				data = json.dumps(workers, indent=4)
				with open("data/workers.json", "w") as f:
							f.write(data)
			else:
				await ctx.send("That isn't a possible job")

@bot.command()
async def remove_worker(ctx, user: discord.Member, job:str=None):
	jobs = ["chef", "delivery", None]
	with open("data/workers.json") as f:
		workers = json.load(f)
	if str(ctx.author.id) in workers["workers"]:
		if "management" in workers["workers"][str(ctx.author.id)]["jobs"]:
			if job in jobs:
				if job:
					del workers["workers"][str(user.id)]["jobs"][job]
					await ctx.send(f"Removed {user.mention} from the {job.title()} job")
				else:
					del workers["workers"][str(user.id)]
					await ctx.send(f"Removed {user.mention} from every job")
				data = json.dumps(workers, indent=4)
				with open("data/workers.json", "w") as f:
							f.write(data)
			else:
				await ctx.send("That isn't a possible job")

@bot.command()
async def invite(ctx):
	await ctx.send("**Breakfast Bro Invite**: https://discordapp.com/api/oauth2/authorize?client_id=366768341026734080&permissions=17409&scope=bot")

@bot.command()
async def server(ctx):
	await ctx.send("https://discord.gg/KRZW9NE")



	


bot.run(private.TOKEN)