import os
import discord
from airtable import Airtable

def get_discord_token():
  return os.getenv("DSB_TOKEN")

def get_discord_server_id():
  return os.getenv("DISCORD_SERVER_ID")

def get_airtable_table(table_name):
  air_table_connection = None
  base_key = os.getenv("AIRTABLE_BASE_NAME")

  #os.getenv("AIRTABLE_USER_TABLE_NAME")
  try:
    air_table_connection = Airtable(base_key, str(table_name))
  except Exception as e:
    print("Exception in getting user airtable: " + str(e))

  if air_table_connection is None:
    print("Airtable not found.")

  return air_table_connection


def is_not_from_self(message, bot):
  if message.author != bot.user:
    return True
  return False

def is_private_message(message):

  try:
    if getattr(message, "guild"):
      # print("Guild:")
      # print(message.guild)
      return False
  except:
    try:
      if getattr(message, "channel"):
        # print("Channel:")
        # print(message.channel)
        return True
    except:
      print("Error in is_private_message(): ")
      print(message)

    
  

#Message processing
def incoming_command_is_valid(command_public_or_private:bool, message, bot):
  intended_private_message = command_public_or_private
  is_actually_sent_private = is_private_message(message)

  if message.author != bot.user: #Only process if it's not from botself!
    if intended_private_message is True:
      if is_actually_sent_private is True:
        print("Valid")
        return True
      else:
        print("Not private when it should be")
        return invalid_command_path_for_dm_command()
    elif intended_private_message is False:
      if is_actually_sent_private is True:
        return True
      else:
        print("Not public when it should be")
        return invalid_command_path_for_dm_command()


def invalid_command_path_for_dm_command():
  embed = discord.Embed(title="Whoops!", color=0xeee657)
  embed.add_field(name="This command is only viable in DMs.", value="Try to message this privately to a bot.")
  return embed

  def invalid_command_path_for_dm_command():
    embed = discord.Embed(title="Ack!", color=0xeee657)
    embed.add_field(name="This command is only viable in a channel.", value="Try to message this from a channel.")
    return embed