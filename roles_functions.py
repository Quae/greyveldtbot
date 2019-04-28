import discord

#IdeasTaster
everyone_id=568108654180696075
idea_taster_id=569240516173234187
fresh_meat_id=569240100882350127
stan_id=569368684888326154
testRole_id=569748451114483712

def get_all_roles_of_user(server: discord.Guild, user_id:int):
  member = server.get_member(user_id)
  roles = member.roles

  return roles

def get_specific_role_by_id(server: discord.Guild, id_of_role :int):
  if not id_of_role:
    print("ERROR in rf get_specific_role_by_id: no id sent")

  if not server:
        print("ERROR, server, in rf get_specific_role_by_id")
  role = server.get_role(id_of_role)

  for role in server.roles:
    if (role.id) == id_of_role:
      return role
  
  print("Unknown error in rf.get_specific_role_by_id")

# def get_specific_role_by_name(name_of_role:str):
#   return discord.utils.guild.roles.find(name_of_role)

# def get_all_users_with_role():
#   return discord.utils.get(get_all_users_with_role)

def get_all_server_roles(server: discord.Guild):
  return server.roles

async def assign_role_to_user(server:discord.Guild, user_id:int, role:discord.guild.Role):
  if (role is not None):
    try:
      #print("Role in rf assign_role_to_user:")
      #print(role)
      member = server.get_member(user_id)
      #print (member)
      await member.add_roles(role)
      #print("New Roles:")
      server.get_member(user_id).roles
      #print("GOT HERE?")
      return 1
    except:
      print("Exception in wf.assign_role_to_user")
  else:
    print("Failed wf.assign_role_to_user")

# if message.content.lower().startswith('/role'):
#     user = message.author

#     if message.channel.is_private or discord.utils.get(user.roles, name="admin") is None:
#         return

#     role = discord.utils.get(user.server.roles, id="437923291047526402")
#     await client.add_roles(user, role)
#   @bot.command(pass_context=True)  
# async def getuser(ctx,*args):
#   server = ctx.message.server
#   role_name = (' '.join(args))
#   role_id = server.roles[0]
#   for role in server.roles:
#     if role_name == role.name:
#       role_id = role
#       break
#   else:
#     await bot.say("Role doesn't exist")
#     return    
#   for member in server.members:
#     if role_id in member.roles:
#       await bot.say(f"{role_name} - {member.name}")
