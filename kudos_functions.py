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
    datapoints = dbf.get_kudos_db_data(member_info)
    #print(user_kudos_info)
    
    # for record in records:
    #      print(record)
      #   for field in record['fields']:
      #     print(field)
    embed.add_field(name="Lifetime Kudos Accrual:", value=datapoints['lifetime_accrual'])
    #embed.add_field(name="Spendable Kudos:", value=datapoints['spendable_kudos'])
    embed.add_field(name="Giftable Kudos:", value=datapoints['giftable_kudos_available'])
    embed.add_field(name="Unique Kudosees:", value=datapoints['unique_kudosees'])
  except Exception as e:
      print ("Error in kudos_report: " + e)

  return embed