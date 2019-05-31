import json
import re
import discord
import auth_functions
from datetime import datetime, timedelta

af = auth_functions

def convert_json_str_to_dict(string_to_convert:str):
  obj = json.loads(string_to_convert)
  print(obj)
  return obj

def filter_str_to_only_digits(original_str):
  new_str = re.sub("\D", "", original_str)
  return new_str

#MEMBER is part of the server, will not work for DMs
def get_member_by_id(server, kudosee_id):
  kudosee_id = filter_str_to_only_digits(kudosee_id)
  print("Kudosee ID:")
  print(kudosee_id)
  kudosee = server.get_member(int(kudosee_id))
  print(kudosee)
  return kudosee

#USER is Discord-wide and works for DMs - WIP
async def get_user_by_id(bot, kudosee_id):
  kudosee_id = int(filter_str_to_only_digits(kudosee_id))
  #kudosee_user_obj = discord.Client.get_user(int(kudosee_id))
  #kudosee_user_obj = await discord.Client.get_user(discord.Client, int(kudosee_id))
  try:
    kudosee_user_obj = await bot.get_user(kudosee_id)
    print("Kudosee OBJ:")
    print(kudosee_user_obj)
    return kudosee_user_obj
  except Exception as e:
      print ("Error in get_user_by_id: ")
      print(e)

def convert_date_to_str_for_db(dateToBeConverted:datetime):
  date = dateToBeConverted.isoformat("|","minutes")
  #print("Converted date:")
  #print(date)
  return date

def convert_str_date_to_date(stringToBeConverted):
  date = datetime.strptime(stringToBeConverted, '%Y-%m-%d|%H:%M')
  #print("Converted date:")
  #print(date)
  return date


# def convert_db_list_to_dict(list_to_convert:list):


#   return datapoints

# def get_fake_user_role_obj(name_of_role, id_of_role):
#   # fake_data = []
#   # fake_data['id'] = int(id_of_role)
#   # fake_data['name'] = name_of_role

#   discord.server
  
#   #fake_user_role = discord.role.Role(guild = None, state = None, data = fake_data)
#   #fake_user_role.id = id_of_role
#   #fake_user_role.name = name_of_role

#   print(fake_user_role)
  
#   return fake_user_role