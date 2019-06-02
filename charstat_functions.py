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

##Breakdown of specific character stats
def single_char_stat_report(member_id:int, char_short_name):
  embed = discord.Embed(title=char_short_name + " is... ", color=0xeee657)

  try:
    datapoints = get_single_char_datapoints(member_id, char_short_name)
    #print("Datapoints inside single_char_stats_report ")
    #print(datapoints)

  
    embed.add_field(name=datapoints['fitness_descriptor'], value=":muscle: Fitness: " + str(datapoints['fitness']))
    embed.add_field(name=datapoints['health_descriptor'], value=":heartbeat: Health: " + str(datapoints['health']))
    embed.add_field(name=datapoints['intelligence_descriptor'], value=":books: Intelligence: " + str(datapoints['intelligence']))
    embed.add_field(name=datapoints['charisma_descriptor'], value=":kiss: Charisma: " + str(datapoints['charisma']))

  except Exception as e:
      print ("Error in single_char_stat_report: ")
      print(e)
      return (False, dbf.get_db_error_in_embed_form())

  return (True, embed)

##List all characters owned by that character by Shortname and descriptors
def user_char_report(member_info):
  return True

##Internal call
def get_single_char_datapoints(member_id, char_short_name):
  lastFour = utils.get_last_four_of_user_id(member_id)
  concatKey = char_short_name + str(lastFour)
  # print("Keycode: ")
  # print(concatKey)
  try:
    data = dbf.get_db_data_or_return_error(dbf.get_char_stat_airtable(), "identifier", concatKey)
    return data
  except Exception as e:
    print ("Error in get_single_char_datapoints: " + e)
    return None