import os
import discord
import auth_functions
import airtable
import pprint
import utils
import json

af = auth_functions


def kudos_report(member_info):

  embed = discord.Embed(title=member_info.name + "'s Kudos Stats" , color=0xeee657)

  try:
    kudos_table = af.get_airtable_table(os.getenv("AIRTABLE_KUDOS_TABLE_NAME"))
    print("Printing report for: " + member_info.name + "| ID: " + str(member_info.id))

    records = kudos_table.search('discord_user_id', member_info.id)
    print("Records: ")
    print(records)

    jsonStr = json.dumps(records)

    json1_data = json.loads(jsonStr)[0]
    datapoints = json1_data['fields']
    print("Datapoints: ")
    print (datapoints)

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
