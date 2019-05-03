#Special thanks to https://gist.github.com/4Kaylum/a1e9f31c31b17386c36f017d3c59cdcc

#IMPORTS
import discord
import asyncio
# import requests
# import random
# import bot_events
from discord.ext import commands

import auth_functions
import roles_functions
import welcoming_functions
import kudos_functions

rf = roles_functions
af = auth_functions
wf = welcoming_functions
kf = kudos_functions


bot = commands.Bot(command_prefix="!")
server = None

# #No responding to self
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
# if message.content == "Hello":
#   await client.send_message(message.channel, "World")

def get_server_obj():
  global server
  return server

def set_server_obj(serverObj):
  global server
  server = serverObj

@bot.event
async def on_ready(pass_context=True):  
  #Change activity
  await bot.change_presence(activity=discord.Game(name="with Quae's head", type=0))

  set_server_obj(bot.guilds[0])
  server = get_server_obj()
  #print(server.roles) #roles
  print("Logged in as " + bot.user.name + " on " + server.name + ", id: " + str(server.id))


@bot.event
async def on_member_join(member):
  await member.send("Welcome to Greyveldt! This is a literate heavy RP server. You will have limited channel access until you agree to abide by our TOS. Reply !TOS or !rules to read our terms of service.")    

# INTERNAL ONLY
@bot.command(pass_context=True)
async def info(ctx): #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Get general info about this server
    '''
    only_for_dms = True
    embed = False

    route_for_command = af.incoming_command_is_valid(only_for_dms, ctx.message, bot)

    if route_for_command is not True:
      embed = route_for_command
  
    elif route_for_command is True:
      embed = discord.Embed(title="Welcome to Greyveldt!", color=0xeee657)

      # give info about you here
      embed.add_field(name="Bossmang & author of the Nesquebot:", value="Quae")

      # Shows the number of servers the bot is member of.
      embed.add_field(name="About Greyveldt:", value="This is an elite RP server for literate, experienced players or literate, intelligent folks who are willing to learn the rules of good co-operative improv. If you have questions, please post them in the #ooc-help channel.")
    if embed != False:
      #print("Deleting old message:")
      await ctx.message.delete()
      message_alert_sent = await ctx.send(embed=embed)
      await asyncio.sleep(5) 
      #print("Deleting bot's old message:")
      await message_alert_sent.delete()
    
@bot.command()
async def tos(ctx): #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Read our terms of service.
    '''
    await ctx.send(embed=wf.get_rules_embed())

@bot.command()
async def rules(ctx): #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Read our terms of service.
    '''
    await ctx.send(embed=wf.get_rules_embed())

@bot.command()
async def wtf(ctx): #tx.message.guild, ctx.message.channel, ctx.message.author
    print("WTF")
    await ctx.send("WTF")


@bot.command()
async def kr(ctx): #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Get a readout of your kudos stats!
    '''
    member_info = ctx.message.author
    embedInfo = kf.kudos_report(member_info)
    try:
      print(embedInfo)
    except Exception as e:
      print("Unable to print embedInfo: " + e)
    #server = get_server_obj()
    await ctx.send(embed=embedInfo)


@bot.command()
async def agree(ctx): #tx.message.guild, ctx.message.channel, ctx.message.author
#do more
  member_id = ctx.message.author.id
  server = get_server_obj()
  user_roles = rf.get_all_roles_of_user(server, member_id)
  
  fresh_meat_role = rf.get_specific_role_by_id(server, rf.fresh_meat_id)
  everyone_id = rf.everyone_id
 
  if (fresh_meat_role is None):
    print("Fresh_meat not valid")
    return 0

  if (wf.brand_new_user(everyone_id, user_roles) == 1):
      await rf.assign_role_to_user(server, member_id, fresh_meat_role)

  else:
    print("Member already has other roles.")

  await ctx.send(embed=wf.tos_agreed_response())
    
  

# # I've moved the command out of on_message so it doesn't get cluttered
# @bot.event
# async def on_message(message):
#     channel = bot.get_channel('458778457539870742')
#     if message.server is None and message.author != bot.user:
#         await bot.send_message(channel, message.content)
#     await bot.process_commands(message)

# # This always sends the same message to the same person.  Is that what you want?
# @bot.command(pass_context=True)
# @commands.is_owner()  # The account that owns the bot
# async def dm(ctx):
#     memberID = "ID OF RECIPIENT"
#     person = await bot.get_user_info(memberID)
#     await bot.send_message(person, "WHAT I'D LIKE TO SAY TO THEM")
#     await bot.delete_message(ctx.message)
    

# async def list_servers():
#     await bot.wait_until_ready()
#     while not bot.is_closed:
#         print("Current servers:")
#         for server in bot.servers:
#             print(server.name)
#         await asyncio.sleep(600)

#Turn on za bot

bot.run(auth_functions.get_discord_token())


#Virtual environ
# In Poweshell: python -m venv bot-env
# bot-env\Scripts\activate.bat
# pip install -U discord.py
