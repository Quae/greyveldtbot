import json
import discord
import auth_functions

af = auth_functions

def convert_json_str_to_dict(string_to_convert:str):
  obj = json.loads(string_to_convert)
  print(obj)
  return obj

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