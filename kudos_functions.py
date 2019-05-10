import os
import discord
import auth_functions
import db_functions
import airtable
import pprint
import utils
import json

af = auth_functions
dbf = db_functions

def kudos_report(member_info):

  embed = discord.Embed(title=member_info.name + "'s Kudos Stats" , color=0xeee657)

  try:
    datapoints = dbf.get_kudos_db_data(member_info.id)
    print (datapoints)

    #ono = bot.get_emoji(521148278079881219)
    #await ctx.send(f"{ono} You said {text}")
    embed.add_field(name=":clap: Lifetime Kudos Accrual:", value=datapoints['lifetime_accrual'])
    embed.add_field(name=" :money_with_wings: Spendable Kudos:", value=datapoints['spendable_kudos'])
    embed.add_field(name=":gift_heart: Giftable Kudos:", value=datapoints['giftable_kudos_available'])
    embed.add_field(name=":handshake: Unique Kudosees:", value=datapoints['unique_kudosees'])
  except Exception as e:
      print ("Error in kudos_report: " + e)

  return embed

def get_giftable_kudos_of_member_by_id(member_id):
  try:
    datapoints = dbf.get_kudos_db_data(member_id)
  except Exception as e:
      print ("Error in get_giftable_kudos_of_member_by_id: " + e)

  return int(datapoints['giftable_kudos_available'])


def set_kudos_column_of_member_by_id(member_id, column_name, num_of_kudos, increment):
  if (increment):
    current = get_giftable_kudos_of_member_by_id(member_id)
    new_total = current + num_of_kudos
  dbf.set_kudos_db_data_by_field_name_for_member_id(member_id, column_name, new_total)


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
          set_kudos_column_of_member_by_id(member_info.id, "giftable_kudos_available", -1, True) #Decrement giver
                                                                        #Increment giver's kudoseeing
          set_kudos_column_of_member_by_id(kudosee_id, "spendable_kudos", 1, True) #Increment kudosee's spendable
          set_kudos_column_of_member_by_id(kudosee_id, "lifetime_accrual", 1, True) #Increment kudosee's lifetime
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

def add_kudos(discord_user_id, amount_to_kudos):
  entry = {}
  entry['discord_user_id'] = discord_user_id
  entry['lifetime_accrual'] = amount_to_kudos