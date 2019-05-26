import discord
import roles_functions

rf = roles_functions

def get_rules_embed():
  embed = discord.Embed(title="Greyveldt Terms of Service", color=0xeee657)
  embed.add_field(name="Don't be a dick", value="- Wheaton's Law")
  embed.add_field(name="1 - Treat People Like People", value="By joining, you agree to treat your fellow players with civility even amidst disagreement. For example, you will be polite when pointing out rules/lore/gameplay violations to other players, and likewise, to respond courteously when/if such is done for you.")
  embed.add_field(name="2 - Adherence to OOC & IC", value="By joining, you agree to abide by OOC vs IC distinction by using specific OOC channels or (( )) for in-channel clarifications. Please minimize OOC banter in IC channels.")
  embed.add_field(name="3 - Be Cooperative", value="By joining, you are agreeing to participate in the created world as an equal partner for improversational play and to abide by existing lore as best as you are able.")
  embed.add_field(name="4 - Keep PG13+ Content Off Public Channels", value="By joining, you agree to keep violent, sexual or otherwise 18+ content in private channels. If a content is requested to be moved to a private channel, please be courteous and do so without complaint. By participating in 18+ content, you are confirming that you are 18+. Greyveldt is not responsible for monitoring or mediating private in-character content. Private OOC bullshit may result in a ban.")
  embed.add_field(name="5 - Copyright Stuff", value="By joining, you acknowledge that your original character alone is yours; lore belongs to Greyveldt and characters belong to their owners.")
  embed.add_field(name="6 - It's A Gentle Monarchy", value="By joining, acknowledge that this server is owned by Quae and Quae has final say in rule enforcement, argument resolution and banning decisionmaking. So figure your shit out amongst yourselves before taking it to her.")
  embed.add_field(name="Opt In", value="To get access to the majority of the server's channels, you need to agree to the above rules by replying '!agree' to your local bot.")
  return embed


def tos_agreed_response():
  embed = discord.Embed(title="Welcome to Greyveldt~!", color=0xeee657)
  embed.add_field(name="You are now '@Fresh Meat!", value="You now have access to additional channels. If not, reach out to #ooc_help!")
  return embed

def tos_already_agreed_response():
  embed = discord.Embed(title="Thanks!", color=0xeee657)
  embed.add_field(name="We appreciate your re-affirmation!", value="Glory, glory, glory.")
  return embed

def brand_new_user(server:discord.Guild, user_id:int, debug):
  if (debug == True):
    print("Faking user roles for debug mode")
    user_roles = [rf.get_specific_role_by_id(server, rf.everyone_id)]
  else:
    user_roles = rf.get_all_roles_of_user(server, user_id)

  everyone_id = rf.everyone_id

  if (len(user_roles) == 1):
    if (debug == True):
      print("Only 1 role:")
      print(str(user_roles[0].id))
      print(str(everyone_id))
    if (user_roles[0].id) == int(everyone_id):
      if (debug == True):
        print ("EVERYNE role found")
      return True

  print ("Multiple roles found:")
  print (user_roles)
  return False