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
import charstat_functions
import kudos_functions
import db_functions
import utils
from datetime import datetime, timedelta
#from discord import Embed, Emoji

rf = roles_functions
af = auth_functions
wf = welcoming_functions
kf = kudos_functions
csf = charstat_functions

dbf = db_functions

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
    await bot.change_presence(
        activity=discord.Game(name="with Quae's head", type=0))

    set_server_obj(bot.guilds[0])
    server = get_server_obj()
    #print(server.roles) #roles
    print("Logged in as " + bot.user.name + " on " + server.name +
          ", bot id: " + str(bot.user.id))


@bot.event
async def on_member_join(member):
  embed = discord.Embed(title="Welcome to Greyveldt!", color=0xeee657)

  embed.add_field(
      name="A literate, heavy RP server with a focus on creative, cooperative story-telling...", value="...set in a janky steampunk/medieval cross genre on a planet unknown to Earth (and vice versa). Medium magic, high fun, no guns or lasers, but we've got ONE WHOLE TRAIN and printing presses!")

  embed.add_field(
      name="Investigate our GitHub hosted wiki...",
      value=" Visit (https://github.com/Quae/greyveldt_lore/blob/master/README.md) for a guide to getting started in the lore world of Greyveldt.")

  embed.add_field(
      name="Read our No-Jerks-Allowed TOS...",
      value="You will have limited channel access until you agree to abide by our TOS. Reply !rules to read our terms of service. You can ask for assistance in the #ooc-help channel if you have any questions, or if you need assistance.")

  await member.send(embed=embed)


# INTERNAL ONLY
@bot.command(pass_context=True)
async def info(
        ctx):  #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Get general info about this server
    '''
    only_for_dms = True
    embed = False

    route_for_command = af.incoming_command_is_valid(only_for_dms, ctx.message,
                                                     bot)

    if route_for_command is not True:
        embed = route_for_command

    elif route_for_command is True:
        embed = discord.Embed(title="Welcome to Greyveldt!", color=0xeee657)

        # give info about you here
        embed.add_field(
            name="Bossmang & author of the Nesquebot:", value="Quae")

        # Shows the number of servers the bot is member of.
        embed.add_field(
            name="About Greyveldt:",
            value=
            "This is an elite RP server for literate, experienced players or literate, intelligent folks who are willing to learn the rules of good co-operative improvisational writing. If you have questions, please post them in the #ooc-help channel."
        )
    if embed != False:
        #print("Deleting old message:")
        await ctx.message.delete()
        message_alert_sent = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        #print("Deleting bot's old message:")
        await message_alert_sent.delete()


@bot.command()
async def rules(
        ctx):  #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Read our terms of service.
    '''
    await ctx.send(embed=wf.get_rules_embed())


@bot.command()
async def wtf(ctx):  #tx.message.guild, ctx.message.channel, ctx.message.author

    # member_info = ctx.message.author
    # member_info.id = "888889"  #fake member info,
    # dbf.create_kudos_table_entry(member_info)
     await ctx.send("WTF executred")


@bot.command()
async def kr(ctx):  #tx.message.guild, ctx.message.channel, ctx.message.author
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
async def daily(ctx):  #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Claim your daily kudos reward!
    '''
    member_info = ctx.message.author
    kudosSuccessAndEmbed = kf.claim_daily_kudos(member_info)

    embedDailyNotice = kudosSuccessAndEmbed[1]

    await ctx.send(embed=embedDailyNotice)

    if (kudosSuccessAndEmbed[0] is True):
        embedInfo = kf.kudos_report(member_info)
        await ctx.send(embed=embedInfo)


@bot.command()
async def charstats(ctx, *args):  #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Print a report on your character's stats
    '''
    member_info = ctx.message.author

    if (args): #return specific char
      char_short_name = str(args[0])

    try:
      if (args[2]):
        member_info = args[2]

    except Exception:
      pass

      charStatsSuccessAndEmbed = csf.single_char_stat_report(member_info.id, char_short_name)
      # print("charstats results: ")
      # print(charStatsSuccessAndEmbed)
    try:
      if (charStatsSuccessAndEmbed[0] is True):
          embedInfo = charStatsSuccessAndEmbed[1]
          await ctx.send(embed=embedInfo)
    except Exception:
      return 

    else: #return list of chars
      return False



@bot.command()
async def gj(
        ctx,
        *args):  #tx.message.guild, ctx.message.channel, ctx.message.author
    '''
    Gift kudos by using '!gj @name'. Only works if you have available kudos to give.
    '''
    member_info = ctx.message.author
    print("Member_info type:")
    print(type(member_info))
    server = get_server_obj()

    try:
        if (args):
            kudosee = utils.get_member_by_id(server, args[0]) #Works
            print("Kudosee type:")
            print(type(kudosee))

            num_of_kudos = 1

            #print(kudosee.id)
            #print(member_info.id)

            kf.gift_kudos(member_info, kudosee.id, num_of_kudos)

            kudosChannelID = 582331378880872448
            kudosChannel = bot.get_channel(kudosChannelID)
            print("Channel:")
            print(kudosChannel)
            #await bot.send_message(kudosChannel, kf.kudos_channel_announcement(member_info, kudosee)) #NO
            embedInfo = kf.kudos_channel_announcement(member_info, kudosee)
            await kudosChannel.send(embed=embedInfo)
        else:
          await ctx.send(embed=kf.explain_gj()) # If no args supplied, explain how it works.
    except Exception as e:
        print("Error in gj command: ")
        print(e)
    # #server = get_server_obj()
    # #await ctx.send(args)  #Will @ the person - '<@151117856958971904>'
    # #await member_info.send(embed=kf.kudos_sent_message)
    #await member_info.send("You've kudosed " + args[0] + ".")

    #await discord.Client.send_message(kudosee, "content")
    #await discord.Client.send(kudosee, "content")
    #print (discord.Client.get_id(572097383438221322))
    #print (discord.Client.get_user(discord.Client, 572097383438221322)) _Connection error
    
    #await kudosee.send("You've been kudosed!")
    #await server.send_message(kudosee, embed=kf.kudos_received_message)
    #kudoseeUser = kudosee.get_user_info()
    #kudoseeChannel = kudoseeUser.create_dm()
    #kudoseeUserObj = discord.client.get_user_by_id(args[0]) #nope
    #kudoseeUserObj = discord.Client.get_user_by_id(args[0]) #nope
 
    #await kudosee.send(embed = kf.kudos_received_message)




@bot.command()
async def agree(
        ctx,
        *args):  #tx.message.guild, ctx.message.channel, ctx.message.author
    #do more
    member = ctx.message.author
    user_id = ctx.message.author.id
    server = get_server_obj()
    #user_roles = rf.get_all_roles_of_user(server, user_id)

    debug = False

    if (args):
        if (args[0] == "debug"):
            print("Debugging is ON!")
            debug = True

    if (dbf.has_agreed_to_tos(user_id)):
      return await ctx.send(embed=wf.tos_already_agreed_response())
    else:
      dbf.set_db_data_by_field_name_for_member_id(dbf.get_user_stat_airtable(), user_id, "tos_agreement_date", utils.convert_date_to_str_for_db(datetime.now()))

      fresh_meat_role = rf.get_specific_role_by_id(server, rf.fresh_meat_id)

      if (fresh_meat_role is None):
          print("Fresh_meat not valid")
          return 0

      if (wf.brand_new_user(server, user_id, debug) is True):
          try:
              print("Waiting assign")
              await rf.assign_role_to_user(server, user_id, fresh_meat_role)
              #print(user_id)
              print("Awaiting DB entry, member.id:")
              print(member.id)
              statResults = dbf.create_user_stat_entry(member)
              if (debug):
                  print("Stats creation:")
                  print(statResults)

              kudosResults = dbf.create_kudos_table_entry(member)
              if (debug):
                  print("Kudos creation:")
                  print(kudosResults)



          except Exception as e:
              print("Error in !agree:")
              print(e)
              return False

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
