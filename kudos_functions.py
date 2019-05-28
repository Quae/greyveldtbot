import os
import discord
import auth_functions
import db_functions
import airtable
import pprint
import utils
import json
from datetime import datetime, timedelta

af = auth_functions
dbf = db_functions

def explain_gj():
  embed = discord.Embed(title="About the Kudos System", color=0xeee657)
  embed.add_field(name="Good roleplay should be rewarded.", value="...and who better to 'kudos' good gameplay than the players! You can use '!gj @name' to let someone know that you really appreciated their pose/creativity.")
  # elaborate
  return embed

def kudos_report(member_info):

  embed = discord.Embed(title=member_info.name + "'s Kudos Stats" , color=0xeee657)

  try:
    datapoints = get_kudos_datapoints(member_info.id)
    #print (datapoints)

    #ono = bot.get_emoji(521148278079881219)
    #await ctx.send(f"{ono} You said {text}")
    embed.add_field(name=":clap: Lifetime Kudos Accrual:", value=datapoints['lifetime_accrual'])
    embed.add_field(name=" :money_with_wings: Spendable Kudos:", value=datapoints['spendable_kudos'])
    embed.add_field(name=":gift_heart: Giftable Kudos:", value=datapoints['giftable_kudos_available'])
    embed.add_field(name=":handshake: Unique Kudosees:", value=datapoints['unique_kudosees'])
  except Exception as e:
      print ("Error in kudos_report: ")
      print (e)

  return embed

def get_kudos_datapoints(member_id:int):
  try:
    return dbf.get_kudos_db_data(member_id)
  except Exception as e:
    print ("Error in get_kudos_datapoints: " + e)

def daily_kudos_claimed(member_info):
  embed = discord.Embed(title="Daily claimed!", color=0xeee657)
  embed.add_field(name=" :money_with_wings: Spendable Kudos:", value="+2")
  embed.add_field(name=":gift_heart: Giftable Kudos:", value="+2")
  return embed

def daily_kudos_cooldown(member_info):
  embed = discord.Embed(title="You can only claim every 24 hours. Try again later." , color=0xeee657)
  return embed

def daily_kudos_failed(member_info):
  embed = discord.Embed(title="Something went horribly wrong. Contact Quae." , color=0xeee657)
  return embed

def kudos_sent_message(member_info, kudosee_id):
  embed = discord.Embed(title=member_info.name + "You've delivered a kudos!" , color=0xeee657)
  return embed

def kudos_channel_announcement(member_info, kudosee_info):
  print("Name of Kudosee: ")
  print(kudosee_info.name)
  embed = discord.Embed(title= ":gift_heart: " + member_info.name + " has kudosed " + kudosee_info.name + "!", color=0xeee657)

  try:
    datapoints = get_kudos_datapoints(kudosee_info.id)

    accrualSentence = "They now have a lifetime accrual of: " + str(datapoints['lifetime_accrual'])
    #accrualSentence = "AAAAAAAAAAAAA"
    embed.add_field(name=accrualSentence, value=":clap: You can also earn kudos by roleplaying well!")
  except Exception as e:
    print ("Error in kudos_channel_announcement: " + e)
    
  return embed

def get_giftable_kudos_of_member_by_id(member_id):
  try:
    datapoints = dbf.get_kudos_db_data(member_id)
  except Exception as e:
      print ("Error in get_giftable_kudos_of_member_by_id: " + e)

  return int(datapoints['giftable_kudos_available'])


def set_kudos_column_of_member_by_id(member_id, column_name, num_of_kudos, increment):
  if (increment):
    print("Col name:")
    print(column_name)
    current = dbf.get_kudos_db_data_by_field_name_for_member_id(member_id, column_name)
    print("Current total:")
    print(current)

    if (current is None):
      current = 0

    new_total = current + num_of_kudos
    print ("New total:")
    print (new_total)
  dbf.set_kudos_db_data_by_field_name_for_member_id(member_id, column_name, int(new_total))

def claim_daily_kudos(member_info):
  dailyAmount = 2
  if (can_claim_daily_kudos(member_info) == True):
    try:
      set_kudos_column_of_member_by_id(member_info.id, "giftable_kudos_available", +dailyAmount, True)
      set_kudos_column_of_member_by_id(member_info.id, "spendable_kudos", +dailyAmount, True)

      currentDate = utils.convert_date_to_str_for_db(datetime.now())
      dbf.set_kudos_db_data_by_field_name_for_member_id(member_info.id, "date_of_last_claim", currentDate)
      return (True, daily_kudos_claimed(member_info))
    except Exception as e:
      print("Error in claim_daily_kudos: ")
      print (e)
      return (False, daily_kudos_failed(daily_kudos_failed))
  else:
    return (False, daily_kudos_cooldown(member_info))

#Every 24 hours, a user can claim 5 spendable kudos
def can_claim_daily_kudos(member_info):
  dateOfLastClaim = dbf.get_kudos_db_data_by_field_name_for_member_id(member_info.id, "date_of_last_claim")

  print("Date of Last Claim: ")
  print(dateOfLastClaim)

  if (dateOfLastClaim is None):
    print("Date of last claim is empty.")
    return True
  else:
    now = datetime.now()
    dateOfLastClaim = utils.convert_str_date_to_date(dateOfLastClaim)

    if now-timedelta(hours=24) >= dateOfLastClaim >= now:
      return True

  return False


def gift_kudos(member_info, kudosee_id, num_of_kudos):
  
  #Default users ONLY give 1 kudos, if we get a num above 1, it's because we passed an admin check earlier & we DON'T check/remove gift kudos from giver
  if (num_of_kudos >= 2):
    print("ADMIN")
    #Straight DB dump
  else:
      #Check if any gift kudos to give, b/c normal user
      giftable_kudos_avail = get_giftable_kudos_of_member_by_id(member_info.id)

      if (giftable_kudos_avail >= 1):
        try:
          #Increment recipient
          set_kudos_column_of_member_by_id(kudosee_id, "spendable_kudos", +1, True) #spendable
          set_kudos_column_of_member_by_id(kudosee_id, "lifetime_accrual", +1, True) #lifetime

          #Decrement giver LAST so it doesn't fail out and eat kudos
          set_kudos_column_of_member_by_id(member_info.id, "giftable_kudos_available", -1, True)
          
        except Exception as e:
          print (e)
      else:
        print ("Unable to gift kudos, no kudos to give.")
  

  
  return 0

def build_blank_kudos_db_entry(member_info):
  datapoints = {}
  datapoints['discord_user_id'] = str(member_info.id)
  datapoints['lifetime_accrual'] = 0
  datapoints['spendable_kudos'] = 0
  datapoints['giftable_kudos_available'] = 0
  datapoints['unique_kudosees'] = 0
  return datapoints

def add_player_given_kudos(discord_user_id, amount_to_kudos):
  entry = {}
  entry['discord_user_id'] = discord_user_id
  entry['lifetime_accrual'] = amount_to_kudos