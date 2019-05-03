import json

def convert_json_str_to_dict(string_to_convert:str):
  obj = json.loads(string_to_convert)
  print(obj)
  return obj

# def convert_db_list_to_dict(list_to_convert:list):


  return datapoints