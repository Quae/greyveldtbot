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