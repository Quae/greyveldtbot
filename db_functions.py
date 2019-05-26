import os
import discord
import auth_functions
import airtable
import pprint
import utils
import json
import kudos_functions

af = auth_functions
kf = kudos_functions

def get_kudos_airtable():
  kudos_table = af.get_airtable_table(os.getenv("AIRTABLE_KUDOS_TABLE_NAME"))
  return kudos_table

def get_user_stat_airtable():
  user_stat_table = af.get_airtable_table(os.getenv("AIRTABLE_USER_TABLE_NAME"))
  return user_stat_table

def set_kudos_db_data_by_field_name_for_member_id(member_id, column_name, value):
  try:
    kudos_table = get_kudos_airtable()
    kudos_table.update_by_field('discord_user_id', member_id, {column_name : value})
  except Exception as e:
    print ("Error in set_kudos_db_data_by_field_name_for_member_id: " + e)

def get_kudos_db_data_by_field_name_for_member_id(member_id, column_name):
  print("Col name in get_kudos_db_data_by_field_name_for_member_id: " + column_name)
  try:
    datapoints = get_kudos_db_data(member_id)
    return datapoints[column_name]

  except Exception as e:
    print ("Error in get_kudos_db_data_by_field_name_for_member_id: " + e)

def get_kudos_db_data(member_id):
  try:

    print("Printing report for: " + str(member_id))

    records = get_kudos_airtable().search('discord_user_id', member_id)
    # print("Records: ")
    # print(records)

    jsonStr = json.dumps(records)

    if (records):
      json1_data = json.loads(jsonStr)[0]
      datapoints = json1_data['fields']
      print("Datapoints: ")
      print (datapoints)
    else:
      raise ValueError('No records found for ' + member_id)

  except Exception as e:
      print ("Error in get_kudos_db_data: " + e)

  return datapoints

def create_user_stat_entry(member_info):
  try:
    #Step 1: confirm that it's not a pre-existing record
    # print("Member Info:")
    # print(member_info)
    # print("Member Info ID:")
    # print(member_info.id)
    member_id = str(member_info.id)
    user_stats_airtable = get_user_stat_airtable()
    print(user_stats_airtable)
    records = user_stats_airtable.search('discord_user_id', member_id)

    if not records:
      print ("New member id:")
      #print (member_info.id)
      newEntry = {'discord_user_id': str(member_info.id), 'discord_name_at_signup': str(member_info.name)}
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