#main.py 
import discord 
from discord.ext import commands,tasks
import youtube_dl
from discord.voice_client import VoiceClient
import math 
import random 
import os
import json
import asyncio 
from random import choice
from io import BytesIO 
from PIL import Image
from itertools import cycle 
from discord.user import User

client = commands.Bot(command_prefix="?")

client.remove_command('help')

bot = commands.Bot(command_prefix='?')

@client.event
async def on_message(message):

	if message.content == "?rebootServer":
		await message.channel.send("Rebooting the Server now...")

	await client.process_commands(message)
	
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name="?help"))
  print (f"{client.user} Is Going To Rock On discord")
  

@client.command(name = 'kick')
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No Reason Provided"):
    try:
        await member.send("You have been kicked from The Server")
    except:
      await ctx.send(member.name + "Has  been kicked from The   Server")
    await member.kick(reason=reason)

 

@client.command(name='ping')
async def ping(ctx):
    await ctx.send(f'**The** Latency: {round(client.latency * 1000)}ms')

@client.command(name='aboutBot')
async def ping(ctx):
    await ctx.send(f'This Bot is created by Swastik Sarkar. \n Bot Host platform - visual Studio Code')
    
@client.command(name='r')
async def ping(ctx):
    await ctx.send(f'\n :warning: RULES TO FOLLOW :warning: \n ➣NO NSFW \n ➣DO NOT MENTION TO MUCH OR YOU WILL BE KICKED \n ➣DO NOT DISRESPECT ANYONE \n ➣SAYING SLANGS CAN KICK YOU \n ➣NO HACKING ALLOWED OR YOU WILL GET INSTANT BAN AND YOU WILL BE REPORTED\nRULES BY SWASTIK SARKAR')

@client.command(name='help')
async def ping(ctx):
    await ctx.send(f'```.py\nCategory:Utility \n\n?Ping - This command is for Knowing server & bot ping(lattency)\n\n?aboutBot - Details about the bot\n\n?rebootServer - This command reboots the server\n\nCategory : Economy \n ?beg - Then only way to get money here\n?bal - To see your ballance \n ?pay [user] - To pay money to someone \n?slots [ammount] - A gamble game ```')


#22WEDsep2021_This_is_the_time_hehe

@client.command(pass_context=True)
async def bal(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]

    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{ctx.author.name}'s balance", color=686868)

    embed.add_field(name= "Wallet Balance", value= wallet_amt,inline = False)
    embed.add_field(name= "Bank Balance", value= bank_amt,inline = False)

    await ctx.send(embed = embed)

@client.command(name="beg" , pass_context=True)
async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    


    earnings = random.randrange(150)

    await ctx.send(f"**Nairo gave you {earnings} coins!!**")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@client.command(pass_context=True)
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Please enter the amount**")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("**You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send("**Amount must be positive**")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"**you withdrew {amount} coins!**")

@client.command(pass_context=True)
async def dep(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Please enter the amount**")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("**You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send("**Amount must be positive**")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"**you deposited {amount} coins!**")


@client.command(pass_context=True)
async def pay(ctx,member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("**Please enter the amount**")
        return

    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]




    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("**You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send("**Amount must be positive**")
        return

    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")

    await ctx.send(f"**you paid {amount} coins!**")

@client.command(pass_context=True)
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
   
    bal = await update_bank(member)

    

    if bal[0]<100:
        await ctx.send("It's not worth it")
        return

    earnings = random.randrange(0, bal[0])
  

    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)

    await ctx.send(f"you robbed and got {earnings} coins!")

@client.command(pass_context=True)
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("You dont have that much money!!")
        return
    if amount<0:
        await ctx.send("Amount must be positive")
        return

    final = []
    for i in range(3):
        a = random.choice([":poop:", ":smile:", ":cherry_blossom:"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
         await update_bank(ctx.author,2*amount)
         await ctx.send("**you won!**")

    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send("**you lost!**")


async def open_account(user):

    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users



async def update_bank(user, change=0,mode = 'wallet'):

    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = users[str(user.id)]["wallet"],users[str(user.id)]["bank"]


    return bal

 
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')

client.run('BOT-TOKEN')
