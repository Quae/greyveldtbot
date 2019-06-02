import os
import discord
import auth_functions
import airtable
import pprint
import utils
import json
import kudos_functions
import utils
from datetime import datetime, timedelta

af = auth_functions
kf = kudos_functions

def get_kudos_airtable():
  kudos_table = af.get_airtable_table(os.getenv("AIRTABLE_KUDOS_TABLE_NAME"))
  return kudos_table

def get_user_stat_airtable():
  user_stat_table = af.get_airtable_table(os.getenv("AIRTABLE_USER_TABLE_NAME"))
  return user_stat_table

def get_char_stat_airtable():
  char_stat_table = af.get_airtable_table(os.getenv("AIRTABLE_CHAR_TABLE_NAME"))
  return char_stat_table

def has_agreed_to_tos(member_id):
  data = get_db_data_by_field_name_for_member_id(get_user_stat_airtable(), member_id, "tos_agreement_date")
  if (data is None):
    return False
  return True


def get_db_error_in_embed_form():
  embed = discord.Embed(title="AAAAAAAAAAAAAAAAAAAAAAAA!" , color=0xeee657)
  embed.add_field(name=" :scream_cat: ERROR!", value="Alert Quae that something happened in the DB call!")
  return embed

## SET DB DATA
#VALUE must be untyped
def set_db_data_by_field_name_for_member_id(table_object, member_id, column_name, value):
  try:
    table_object.update_by_field('discord_user_id', member_id, {column_name : value})
  except Exception as e:
    print ("Error in set_db_data_by_field_name_for_member_id: ")
    print (e)

## GET DB DATA
def get_db_data_by_field_name_for_member_id(table_object, member_id, column_name):
  print("Col name in get_db_data_by_field_name_for_member_id: " + column_name)
  try:
    datapoints = get_db_data_or_return_error(table_object, 'discord_user_id', member_id) #Update to pull specific field
    #datapoints = table_object.search('discord_user_id', member_id, column_name, )
    return datapoints[column_name]

  except Exception as e:
    print ("Error in get_db_data_by_field_name_for_member_id: ")
    print(e)

def get_db_data_or_return_error(table_object, column_name, key):
  records = table_object.search(column_name, key)
  jsonStr = json.dumps(records)

  if (records):
    json1_data = json.loads(jsonStr)[0]
    datapoints = json1_data['fields']
    print("Datapoints: ")
    print (datapoints)
    return datapoints
  else:
    print('No records found for ' + key )
    return None

def create_user_stat_entry(member_info):
  try:
    #Step 1: confirm that it's not a pre-existing record
    member_id = str(member_info.id)
    user_stats_airtable = get_user_stat_airtable()
    print(user_stats_airtable)
    records = user_stats_airtable.search('discord_user_id', member_id)

    if not records:
      print ("New member id:")
      #print (member_info.id)
      newEntry = {'discord_user_id': str(member_info.id), 'discord_name_at_signup': str(member_info.name), 'tos_agreement_date': utils.convert_date_to_str_for_db(datetime.now())}
      print("New Entry:")
      print(newEntry)
      
      user_stats_airtable.insert(newEntry)
      return True
    else:
      print ("Pre-existing entry")
      return False

  except Exception as e:
    print ("Error in create_user_stat_entry: " + e)

def create_kudos_table_entry(member_info):
  try:
    member_id = str(member_info.id)
    print("Member ID:")
    print(member_id)
    kudos_airtable = get_kudos_airtable()
    print(kudos_airtable)
    records = kudos_airtable.search('discord_user_id', member_id)

    print(records)

    if not records:
      print(82)
      #newEntry = {'discord_user_id': str(member_info.id)}
      newEntry = kf.build_blank_kudos_db_entry(member_info)
      print("New Entry:")
      print(newEntry)
      
      success = kudos_airtable.insert(newEntry)
      print(success)
      return True
  except Exception as e:
    print ("Error in create_kudos_table_entry: " + e)
    return False