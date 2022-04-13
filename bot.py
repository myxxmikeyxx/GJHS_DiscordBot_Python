from gettoken import *
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
# discord.ext.commands.errors.MissingPermissions
from discord.ext.commands import CommandNotFound
# discord.ext.commands.errors.CommandNotFound
import logging
from typing import Optional

# Need to do for every command
# https://stackoverflow.com/questions/47859913/how-do-i-edit-a-discord-bot-commands-description-as-shown-in-the-default-help-c
# Need to add to guild join so it makes a new json file or a guild ID and stores multiple info like links, teams joined in channels, coaches, etc
# https://stackoverflow.com/questions/41210126/python-adding-fields-and-labels-to-nested-json-file

# Add: User joining/leaving guild
# https://gist.github.com/Anubhav1603/e0be4e51c3e2ff50ffe9c2b46e1f667f
# https://gist.github.com/Anubhav1603/e0be4e51c3e2ff50ffe9c2b46e1f667f#user-joiningleaving-guild

# https://discordpy.readthedocs.io/en/stable/logging.html
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = gettoken()
TOKEN = token["token"]

# https://stackoverflow.com/questions/64513680/discord-py-prefix-command
def get_prefix(client, message): ##first we define get_prefix
    with open('config.json', 'r') as f: ##we open and read the config.json, assuming it's in the same file
        prefixes = json.load(f) #load the json as prefixes
    return prefixes[str(message.guild.id)]["prefix"] #recieve the prefix for the guild id given

# https://stackoverflow.com/questions/64221377/discord-py-rewrite-get-member-function-returning-none-for-all-users-except-bot
# intents = discord.Intents.default()
# intents.members = True
bot = commands.Bot(command_prefix= (get_prefix))

# Orginal join guild
# @bot.event
# async def on_guild_join(guild): #when the bot joins the guild
#     prefix = 'bot!'#default prefix
#     for channel in guild.text_channels:
#         if channel.permissions_for(guild.me).send_messages:
#             await channel.send(f'Hello, I\'m {bot.user}. Thanks for inviting me. \n'
#                 f'Use {prefix} for the start any of my commands.\n'
#                 f'Administrators can change this by using "{prefix}changeprefix" command ')
#         break
#     with open('config.json', 'r') as f: #read the config.json file
#         prefixes = json.load(f) #load the json file
    
#     prefixes[str(guild.id)] = prefix
#     # add extra code here to make a name of guild id with data stored inside.
#     # https://stackoverflow.com/questions/52281671/how-do-i-created-nested-json-object-with-python
#     # https://www.geeksforgeeks.org/json-with-python/
#     prefixes["Guilds"] = guild.id

#     with open('config.json', 'w') as f: #write in the config.json "message.guild.id": "bl!"
#         json.dump(prefixes, f, indent=4) #the indent is to make everything look a bit neater

# Tweaked join guild for making guild friendlies channels
# https://www.w3schools.com/python/python_dictionaries_add.asp
    # add extra code here to make a name of guild id with data stored inside.
    # https://stackoverflow.com/questions/52281671/how-do-i-created-nested-json-object-with-python
    # https://www.geeksforgeeks.org/json-with-python/
@bot.event
async def on_guild_join(guild): #when the bot joins the guild
    prefix = 'bot!'#default prefix
    chan_names = "Friendlies"
    channels = {}
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f'Hello, I\'m {bot.user}. Thanks for inviting me. \n'
                f'Use `{prefix}` for the start any of my commands.\n'
                f'Administrators can change this by using `{prefix}changeprefix "newPrefix"` command ')
        break
    with open('config.json', 'r') as f: #read the config.json file
        # Create Python object from JSON string
        data = json.load(f) #load the json file
    
    # adds a prefix under the guilds ID
    channels.update({ "prefix" : prefix })
    # adds links group and adds the friendlies to that list
    temp = {}
    for i in data[chan_names]:
        temp.update({ i : data[chan_names][i]})
    channels.update({ "links" : temp })


    # adds friendlies as catrgories in any new guilds
    for i in data[chan_names]:
        channels.update({ i : {} })
    data[str(guild.id)] = channels

    with open('config.json', 'w') as f: #write in the config.json "message.guild.id": "bl!"
        json.dump(data, f, indent=4) #the indent is to make everything look a bit neater

# @bot.event
# async def on_guild_remove(guild): #when the bot is removed from the guild
#     with open('config.json', 'r') as f: #read the file
#         prefixes = json.load(f)

#     prefixes.pop(str(guild.id)) #find the guild.id that bot was removed from

#     with open('config.json', 'w') as f: #deletes the guild.id as well as its prefix
#         json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('config.json', 'r') as f: #read the file
        data = json.load(f)
# might need to tweak later but should just remove the whole guild
    data.pop(str(guild.id)) #find the guild.id that bot was removed from
    # popped = data.pop(str(guild.id)) #find the guild.id that bot was removed from
    # print(popped)
    with open('config.json', 'w') as f: #deletes the guild.id as well as its prefix
        json.dump(data, f, indent=4)


# https://stackoverflow.com/questions/64513680/discord-py-prefix-command
# https://youtu.be/Hh9MYiaV9U8?t=174
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
# @bot.event
async def changeprefix(ctx, prefix): #command: bl!changeprefix ...
    # https://stackoverflow.com/questions/51240878/discord-bot-check-if-user-is-admin
    if ctx.message.author.guild_permissions.administrator:
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)]["prefix"] = prefix

        with open('config.json', 'w') as f: #writes the new prefix into the .json
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to: {prefix}') #confirms the prefix it's been changed to
    else:
        ctx.send(f'{ctx.message.author.mention} does not have permission for this command!')


# later split this into singular and plural for setting all friendlies and for setting just that chats
@bot.command(aliases=["setrules", "setlink", "setlinks", "gamerule", "gamerules", "setdoc", "setdocs", "setdocument", "setdocuments"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def setrule(ctx, args1: Optional[str] = None):
    if ctx.message.author.guild_permissions.administrator:
        # checks if the cmd was in the correct category and if not breaks right away
        place = right_category(ctx)
        if place == False:
            return
        guild = ctx.message.guild
        chat_location = ctx.channel
        # if no link is passed then set it to empty quotes
        if args1 == None:
            args1 = ""
        cat_name = "Friendlies"
        with open('config.json', 'r') as f:
            data = json.load(f)
            data[str(guild.id)]["links"].update({chat_location.name : args1})
        with open('config.json', 'w') as f: #writes the new prefix into the .json
            json.dump(data, f, indent=4)
    else:
        ctx.send(f'{ctx.message.author.mention} does not have permission for this command!')

@bot.command(aliases=["rule", "showrule", "showrules", "showlink", "showlinks", "showgamerule", "showgamerules", "showdoc", "showdocs", "showdocument", "showdocuments"])
async def rules(ctx):
    # checks if the cmd was in the correct category and if not breaks right away
    place = right_category(ctx)
    if place == False:
        return
    guild = ctx.message.guild
    chat_location = ctx.channel
    cat_name = "Friendlies"
    # set this bellow
    chat_name = ""
    with open('config.json', 'r') as f:
        data = json.load(f)
        rule = data[str(guild.id)]["links"][chat_location.name]
        for key,value in data["Names"].items():
            if key == chat_location.name:
                chat_name = value
    embed = discord.Embed(title=f'{chat_name}')
    # embed.add_field(name = 'Number of Teams', 
    #     value= '\n'.join([f'{x}' for x in team_num]), 
    #     inline = True)
    embed.add_field(name="Rules", value=f'{rule}', inline = True)
    # embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)
    # prints message in chat
    await chat_location.send(embed=embed)

@bot.command(aliases=["menu", "showmenu", "showcommands", "commands", "coachcmds", "coachcommands", "cmds", "showcmds"])
async def showcmd(ctx):
    guild = ctx.message.guild
    chat_location = ctx.channel
    cmds = {}
    with open('config.json', 'r') as f:
        data = json.load(f)
        for key,value in data["cmds"].items():
            cmds.update({key : value})
    embed = discord.Embed(title='Bot Commands')
    embed.add_field(name="Command",
        value= '\n\n'.join([f'{key}' for key,value in cmds.items()]), 
        inline = True)
    white_space = '\x7f'
    embed.add_field(name = u'{0}'.format(white_space), 
        value= u'{0}'.format(white_space), 
        inline = True)
    embed.add_field(name="Description",  
        value = '\n\n'.join([f'{value}' for key,value in cmds.items()]), 
        inline = True)
    # embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)
    # prints message in chat
    await chat_location.send(embed=embed)

# https://stackoverflow.com/questions/62239816/how-do-i-make-the-bot-respond-when-someone-mentions-it-discord-py
@bot.event
async def on_message(msg):
    if bot.user.mentioned_in(msg):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)
            pre = prefixes[str(msg.guild.id)]["prefix"]
            # await msg.channel.send(f'{bot.user} is online!')
            # Useful character for "code sample": `code here`
            await msg.channel.send(f'Your command prefix is: {pre}\n'
                f'You can type `{pre}help` for more help')
    # https://stackoverflow.com/questions/49331096/why-does-on-message-stop-commands-from-working
    # This is needed or else no commands will work. You can just ignore when the bot is pinged but it is helpful
    await bot.process_commands(msg)

@bot.command(aliases=["jointeams","jointeam"])
async def join(ctx, args1: Optional[int] = None):
    # checks if the cmd was in the correct category and if not breaks right away
    place = right_category(ctx)
    if place == False:
        return
    guild = ctx.message.guild
    # username = ctx.message.author.name
    # print(username)
    user_id = ctx.message.author.id
    # print(user_id)
    # https://www.codegrepper.com/code-examples/python/discord+py+get+user+by+id
    # will need to use this when doing a ping and anwhere we are getting the user
    user = await bot.fetch_user(user_id)
    cat_name = "Friendlies"
    team_dict = {}
    if args1 == None:
        args1 = 1
    # You are in the right category, now need to check what chat
    chat_location = None
    guild_id = None
    # channel = discord.utils.get(guild.text_channels, name=cat_name)
    # message.channel
    # print("\n================\n", ctx.channel, "\n================\n")
    with open('config.json', 'r') as f:
        config = json.load(f)
        for i in config[cat_name]:
            if i == str(ctx.channel):
                # print("Match Channel Name")
                chat_location = ctx.channel
                break
        # print(chat_location)
        # print(guild.id)
        # print(type(guild.id))
        # print("=====================")
        for x in config:
            # print(type(x))
            if x == str(guild.id):
                # print("Matched Guild ID")
                guild_id = x
                break
        team_dict = config[guild_id][chat_location.name] 
        team_dict.update({user_id : args1})
        config[guild_id][chat_location.name] = team_dict
        # print(team_dict)
        # print("=====================")
        # print(f'config-{guild_id}-{chat_location.name}\n', config[guild_id][chat_location.name])
        # print("=====================")
        # print(config[guild_id][chat_location.name])
        with open('config.json', 'w') as f: #writes the new prefix into the .json
            json.dump(config, f, indent=4)
        if args1 == 1:
            await chat_location.send(f'{user.mention} has joined {chat_location.name} with {args1} team.')
        else:
            await chat_location.send(f'{user.mention} has joined {chat_location.name} with `{args1}` teams.')
        
@bot.command(aliases=["removeteams","removeteam", "leave", "leavematch", "leavemaking"])
async def remove(ctx, args1: Optional[int] = None):
    place = right_category(ctx)
    if place == False:
        return
    guild = ctx.message.guild
    username = ctx.message.author.name
    user_id = ctx.message.author.id
    user = await bot.fetch_user(user_id)
    cat_name = "Friendlies"
    team_dict = {}
    if args1 == None:
        args1 = 0
    chat_location = None
    guild_id = None
    with open('config.json', 'r') as f:
        config = json.load(f)
        for i in config[cat_name]:
            if i == str(ctx.channel):
                chat_location = ctx.channel
                break
        for x in config:
                # print(type(x))
                if x == str(guild.id):
                    # print("Matched Guild ID")
                    guild_id = x
                    break
        if str(user_id) in config[guild_id][chat_location.name]:
            print(f"Key {user_id} exist in JSON data")
        else:
            await chat_location.send(f'{user.mention} has no teams in this channel to remove!')
            print(f"Key {user_id} not found in JSON data.")
            return
        if args1 == 0:
            all_teams = config[guild_id][chat_location.name][str(user_id)]
            config[guild_id][chat_location.name].pop(str(user_id))
            with open('config.json', 'w') as f: #writes the new prefix into the .json
                json.dump(config, f, indent=4)
            await chat_location.send(f'{user.mention} has left {chat_location.name} with `{all_teams}` teams.')
        else:
            print(config[guild_id][chat_location.name][str(user_id)])
            current_val = config[guild_id][chat_location.name][str(user_id)]
            if current_val < args1:
                all_teams = config[guild_id][chat_location.name][str(user_id)]
                with open('config.json', 'w') as f: #writes the new prefix into the .json
                    json.dump(config, f, indent=4)
                await chat_location.send(f'{user.mention} has left {chat_location.name} with `{all_teams}` teams.')
            else:
                config[guild_id][chat_location.name].update({str(user_id) : current_val - args1})
                with open('config.json', 'w') as f: #writes the new prefix into the .json
                    json.dump(config, f, indent=4)
                if args1 == 1:
                    if (current_val - args1) > 1:
                        await chat_location.send(
                            f'{user.mention} has removed `{args1}` team.\n'
                            f'{username} has `{current_val - args1}` teams left.'
                        )
                    else:
                        await chat_location.send(
                            f'{user.mention} has removed `{args1}` team.\n'
                            f'{username} has `{current_val - args1}` team left.'
                        )
                if args1 > 1:
                    if (current_val - args1) > 1:
                        await chat_location.send(
                            f'{user.mention} has removed `{args1}` teams.\n'
                            f'{username} has `{current_val - args1}` teams left.'
                        )
                    else:
                        await chat_location.send(
                            f'{user.mention} has removed `{args1}` teams.\n'
                            f'{username} has `{current_val - args1}` team left.'
                        )

# need to still do a list of coaches and number of teams
@bot.command(aliases=["listteams", "listteam", "listcoach", "listcoaches"])
async def list(ctx):
    place = right_category(ctx)
    if place == False:
        return
    guild = ctx.message.guild
    # username = ctx.message.author.name
    user_id = ctx.message.author.id
    # user = await bot.fetch_user(user_id)
    chat_location = ctx.channel
    with open('config.json', 'r') as f:
        data = json.load(f)
        # https://www.reddit.com/r/Discord_Bots/comments/ljeuz0/how_to_get_member_object_from_id_discordpy/
    # https://stackoverflow.com/questions/57212859/how-to-align-fields-in-discord-py-embedded-messages
    # https://stackoverflow.com/questions/68852747/discord-py-add-multiple-values-with-for-loop-to-single-embedfield
    embed = discord.Embed(title=f'{chat_location.name}')
    cnt = 1
    coaches = []
    team_num = []
    for key,val in data[str(guild.id)][chat_location.name].items():
        # print(key)
        # print(val)
        # https://github.com/Rapptz/discord.py/issues/5867
        # https://discordpy.readthedocs.io/en/latest/api.html#discord.Guild.get_member
        # https://stackoverflow.com/questions/64221377/discord-py-rewrite-get-member-function-returning-none-for-all-users-except-bot
        # member = guild.get_member(int(key))
        try:
            member = await guild.fetch_member(int(key))
            nick = member.nick
            if nick != None:
                coaches.append(nick)
                team_num.append(val)
            else:
                coach = await bot.fetch_user(key)
                coaches.append(coach)
                team_num.append(val)
        except:
            coach = await bot.fetch_user(key)
            coaches.append(coach)
            team_num.append(val)
            pass
    if len(coaches) <= 0:
        await chat_location.send("`No Coaches to list.`")
        return

    # change thumbnail based on which chat  
    # embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
    # create fields in the list
    embed.add_field(name = 'Coaches', 
        value= '\n'.join([f'{i}' for i in coaches]), 
        inline = True)
    # https://stackoverflow.com/questions/54437054/set-of-hidden-unicode-characters-in-a-string
    # really this is a del character 
    white_space = '\x7f'
    embed.add_field(name = u'{0}'.format(white_space), 
        value= u'{0}'.format(white_space), 
        inline = True)
    
    embed.add_field(name = 'Number of Teams', 
        value= '\n'.join([f'{x}' for x in team_num]), 
        inline = True)

    # embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

    # prints message in chat
    await chat_location.send(embed=embed)

# still need to do a sort json keys by highest VALUE then pair them up (photos on phone)
@bot.command(aliases=["matchteams", "matchcoaches"])
async def match(ctx):
    if ctx.message.author.guild_permissions.administrator:
        place = right_category(ctx)
        if place == False:
            return
        guild = ctx.message.guild
        user_id = ctx.message.author.id
        chat_location = ctx.channel
        teams = {}
        role_name = "Coaches"
        coaches_role = discord.utils.get(guild.roles,name=role_name)
        # print(coaches_role)
        with open('config.json', 'r') as f:
            data = json.load(f)
        teams = sort_teams(guild, chat_location)
        # print(len(teams))
        # need to take the first coach and match with second coach and if it has leftoers then repeate
        # create a function that does the matching and subtracting and return leftovers
        # print(teams.items())
        if len(teams) <= 1:
            if len(teams) == 0:
                await chat_location.send("`No coaches joined to create a match.`")
                return
            await chat_location.send("`Not enough coaches to create match.`")
            return
        # https://www.delftstack.com/howto/python/get-first-key-in-dictionary-python/#:~:text=By%20the%20first%20key%2C%20we,key%20using%20the%20next%20function.
        # get the first value in teams
        firstkey = next(iter(teams))
        firstval = teams[firstkey]
        print(firstkey, ":" , firstval)

        # pop out first value to get second value
        teams.pop(firstkey)

        # get second value
        secondkey = next(iter(teams))
        secondval = teams[secondkey]
        print(secondkey, ":" , secondval)

        # pop out second value to get it ready for the while loop
        teams.pop(secondkey)
        true = True
        while true:
            left = match_teams(firstkey, firstval, secondkey, secondval)
            # get the returned values
            temp_secondkey = next(iter(left))
            temp_secondval = left[temp_secondkey]
            if temp_secondval == 0:
                print("inside temp_secondval == 0")
                # need to msg before we check or else msg is never sent
                # put msg that first key and first value have X number of matches with second key and second val
                coach1 = await bot.fetch_user(int(firstkey))
                coach2 = await bot.fetch_user(int(secondkey))
                await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                            f'`Away:` {coach2.mention}\n'
                                            f'`Setup {secondval} matche(s).\n`'
                                            "GLHF!")
                if len(teams) == 1:
                    # put msg that left over team needs X number of matches
                    msgKey = next(iter(teams))
                    coach1 = await bot.fetch_user(int(msgKey))
                    msgValue = teams[msgKey]
                    await chat_location.send('!!Attention!!\n'
                                            f'{coaches_role.mention}\n'
                                            f'{coach1.mention} needs {msgValue} of matche(s).')
                    true = False
                    break
                elif  len(teams) == 0:
                    # no teams left need a match, break
                    print("no teams left, printing msg about matches")
                    coach1 = await bot.fetch_user(int(firstkey))
                    coach2 = await bot.fetch_user(int(secondkey))
                    await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                                f'`Away:` {coach2.mention}\n'
                                                f'`Setup {secondval} matche(s).\n`'
                                                "GLHF!")
                    true = False
                    break
                # need to do this after everything above if it makes it here
                # get next two keys and values and set them to firstkey firstval secondkey secondval
                firstkey = next(iter(teams))
                firstval = teams[firstkey]
                print(firstkey, ":" , firstval)
                # pop out first value to get second value
                teams.pop(firstkey)
                secondkey = next(iter(teams))
                secondval = teams[secondkey]
                print(secondkey, ":" , secondval)
                # pop out second value
                teams.pop(secondkey)
            elif temp_secondval > 0:
                print("inside temp_secondval > 0")
                # need to msg before we check or else msg is never sent
                # put msg that first key and first value have X number of matches with second key and second val
                coach1 = await bot.fetch_user(int(firstkey))
                coach2 = await bot.fetch_user(int(secondkey))
                await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                            f'`Away:` {coach2.mention}\n'
                                            f'`Setup {secondval} matche(s).\n`'
                                            "GLHF!")
                if len(teams) == 0:
                    # put msg that secondkey and secondval needs X number of matches still
                    coach2 = await bot.fetch_user(int(firstkey))
                    await chat_location.send('!!Attention!!\n'
                                            f'{coaches_role.mention}\n'
                                            f'{coach2.mention} needs {secondval} of matche(s).')
                    true = False
                    break
                # get next key value as firstkey firstval
                print("had reminder teams in json")
                firstkey = next(iter(teams))
                firstval = teams[firstkey]
                print(firstkey, ":" , firstval)
                # pop value to remove it
                teams.pop(firstkey)
                secondkey = temp_secondkey
                secondval = temp_secondval
            else:
                print("Should not be here!")
            # true = False
        data[str(guild.id)].update({chat_location.name : {} })
        with open('config.json', 'w') as f: #write in the config.json "message.guild.id": "bl!"
            json.dump(data, f, indent=4) #the indent is to make everything look a bit neater
        print(f"all data from {chat_location.name} has been cleared")
    else:
        ctx.send(f'{ctx.message.author.mention} does not have permission for this command!')


    # for i in teams:
    #     print(i)
    #     teams.pop(str(i))
    #     for x in teams:
    #         print(x)
    #         teams.pop(str(x))
    #         # matched = await match_teams(i)
    # use  .update for a dict to change the teams left for the returned value
    #     channels.update({ "prefix" : prefix })
    # for i in data[chan_names]:
    #     channels.update({ i : {} })
    # data[str(guild.id)] = channels

def match_teams(firstkey, firstval, secondkey, secondval):
    temp = {}
    leftoverval = 0
    try:
        leftoverval = firstval - secondval
        if leftoverval > 0:
            print("has leftovers")
            temp.update({firstkey : leftoverval})
        elif leftoverval == 0:
            temp.update({firstkey : leftoverval})
            print("no leftovers")
    except Exception as e:
        # https://blog.finxter.com/how-to-catch-and-print-exception-messages-in-python/#:~:text=To%20catch%20and%20print%20an,use%20it%20for%20further%20processing.
        # ... PRINT THE ERROR MESSAGE ... #
        print(e)
    # need to check if returned value is 0 if it is then pass two new values
    print(temp)
    return temp

# https://www.geeksforgeeks.org/python-sort-json-by-value/ try example #2
def sort_teams(guild, channel):
    temp = {}
    with open('config.json', 'r') as f:
        data = json.load(f)
    temp = dict(sorted(data[str(guild.id)][channel.name].items(), key=lambda item: item[1], reverse=True))
    # print(temp.items())
    return temp

def right_category(ctx):
    # https://stackoverflow.com/questions/68235517/creating-a-channel-in-specific-category-the-category-id-is-should-be-variable
    guild = ctx.message.guild
    cat_name = "Friendlies"
    category = discord.utils.get(guild.categories, name=cat_name)
    # if guild.categories != category:
    if str(category) != cat_name:
        # print("Not in the right location.")
        return False
    # print("Right Location")
    return True

# https://stackoverflow.com/questions/48141407/how-would-i-make-my-python-3-6-1-discord-bot-create-a-new-text-channel-in-a-serv
# https://www.codegrepper.com/code-examples/python/discord+py+group+chat
# https://stackoverflow.com/questions/48172961/make-a-category-on-a-server-with-a-bot-inside-the-discord-py-api
@bot.command(aliases=["setup", "createchannels", "makechannels"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def setupchannels(ctx):
        # https://stackoverflow.com/questions/51240878/discord-bot-check-if-user-is-admin
    if ctx.message.author.guild_permissions.administrator:
        guild = ctx.message.guild
        message = ""
        cat_name = "Friendlies"
        # add a section to create a coaches role so it can easily ping them all
        # https://www.codegrepper.com/code-examples/javascript/discord.js+add+role+to+user need for python
        # https://stackoverflow.com/questions/62819810/get-role-by-name-discord-py-rewrite
        role_name = "Coaches"
        role = discord.utils.get(guild.roles,name=role_name)
        if role == None:
            await guild.create_role(name=role_name)
            await ctx.send(f'Role `{role_name}` has been created')
        else:
            await ctx.send(f'Role `{role_name}` already exist.')
        returned_values = check_category(guild, cat_name, message)
        print(returned_values)
        try:
            message = returned_values[0]
            create_cat = returned_values[1]
            await create_cat
        except:
            # print("returned_values has no first index")
            pass
        with open('config.json', 'r') as f:
            config = json.load(f)
            message += "Channels Created: \n`"
            # https://stackoverflow.com/questions/67442352/discord-py-how-to-check-text-channel
            # https://stackoverflow.com/questions/49446882/how-to-get-all-text-channels-using-discord-py
            # https://stackoverflow.com/questions/63695135/how-to-get-a-category-by-its-id
            # https://stackoverflow.com/questions/64200134/renaming-and-moving-channel-to-a-different-category-with-a-command
            # https://discordpy.readthedocs.io/en/stable/api.html#discord.CategoryChannel.move
            category = discord.utils.get(guild.categories, name=cat_name)
            print(category)
            cnt = 0
            for i in config[cat_name]:
                try:
                    channel = discord.utils.get(guild.text_channels, name=i)
                    if channel == None:
                        # https://github.com/Rapptz/discord.py/issues/5818
                        print(i)
                        channel = guild.create_text_channel(i, category=category, position=cnt)
                        await channel
                        message += f"{i}\n"
                    else:
                        print(i + " already exist")
                        message += f"{i} (already exist, skipping)\n"
                    cnt += 1
                    pass
                except:
                    cnt += 1
                    pass
        message += "`"
        text_channel_list = get_text_channels(guild)
        await ctx.send(message)
    else:
        ctx.send(f'{ctx.message.author.mention} does not have permission for this command!')

def check_category(guild, cat_name, message):
    category = discord.utils.get(guild.categories, name=cat_name)
    if category is None: #If there's no category matching with the `name`
        cat = guild.create_category(cat_name) #Creates the category
        message += "Category Friendlies Not Found, Creating\n"
        return [message, cat]
    else: #Else if it found the categoty
        message += "Category Friendlies Found (Skipping Creation)\n" #Dosent make the category, instead it pass the creation of the category
        return [message]

# https://stackoverflow.com/questions/65012373/how-to-get-text-channels-from-specific-server
def get_text_channels(guild):
    text_channel_list = []
    for channel in guild.text_channels:
        text_channel_list.append(channel.name)
    return text_channel_list



#Outputs to console when the bot is ready and joined server
@bot.event
async def on_ready():
    print(
        f'{bot.user} is online.\n'
    )
    # print('We have logged in as {0.user}'.format(bot))
    
@bot.command(aliases=["listguilds","guildslist","showallguilds"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def showguilds(ctx):
        # https://stackoverflow.com/questions/51240878/discord-bot-check-if-user-is-admin
    if ctx.message.author.guild_permissions.administrator:
        # hard coded my user ID so only I can see the connected guilds can be changed, removed, or commented out
        if ctx.author.id != 225769313183727617:
            return
        message = ""
        num = 1
        for guild in bot.guilds:
    # https://stackoverflow.com/questions/57212859/how-to-align-fields-in-discord-py-embedded-messages
            # reformat using embed = discord.Embed(title=f'{chat_location.name}')
            message += f"{num}.{guild.name}  - ID: {guild.id}\n"
            num = num + 1
        await ctx.send(message)
    else:
         ctx.send(f'{ctx.message.author.mention} does not have permission for that command.')

@bot.command(aliases=["updateconf","confupdate","configupdate"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def updateconfig(ctx):
        # https://stackoverflow.com/questions/51240878/discord-bot-check-if-user-is-admin
    if ctx.message.author.guild_permissions.administrator:
        message = ""
        num = 1
        
        with open('config.json', 'r') as f:
            data = json.load(f)
            temp_prefix = ""
            temp_links = {}
            temp_friendlies = {}
        for guild in bot.guilds:
            # get ride of this for loop and just put this all in a try and the execpt would that the server is not in the config
            for key,value in data[str(guild.id)].items():
                # print(key , " - ", value)
                if key == "prefix":
                    temp_prefix = data[str(guild.id)]["prefix"]
                    pass
                if key == "links":
                    # this will only add items from friendlies if any are removed then it will delete the last from all the guilds (breaks it)
                    temp_links = links_update(str(guild.id))
                    pass
            # call seperate def to itterate through and update the guilds from friendlies groups
            # the print should just show that it only has friendlies titles
            # print("Print Me:\n", data[str(guild.id)])
            
            # removes the prefix and links for the next step
            data[str(guild.id)].pop("prefix")
            data[str(guild.id)].pop("links")
            # the next step
            temp_friendlies = guilds_update(str(guild.id))
            data.pop(str(guild.id))
            # this restores all values
            data.update({str(guild.id): {}})
            data[str(guild.id)]["prefix"] = temp_prefix
            data[str(guild.id)]["links"] = temp_links
            data[str(guild.id)] = temp_friendlies
            message += f"{num}.{guild.name} = Updated Config\n"
            num = num + 1
        await ctx.send(message)
        with open('config.json', 'w') as f: #write in the config.json "message.guild.id": "bl!"
            json.dump(data, f, indent=4) #the indent is to make everything look a bit neater
    else:
         ctx.send(f'{ctx.message.author.mention} does not have permission for that command.')

def links_update(guild_id):
    temp_key = []
    temp_value = []
    temp_key2 = []
    temp_value2 = []
    updated_links = {}
    with open('config.json', 'r') as f:
        temp = json.load(f)
    for key,value in temp["Friendlies"].items():
        temp_key.append(key)
        temp_value.append(value)
    for key2,value2 in temp[guild_id]["links"].items():
        temp_key2.append(key2)
        temp_value2.append(value2)
    # https://realpython.com/python-enumerate/
    cnt = 0
    for x in temp_key:
        # print(cnt , " - ", x)
        try:
            temp_key2.index(x)
            # print("Match Found")
            updated_links.update({temp_key2[cnt] : temp_value2[cnt]})
            cnt += 1
        except:
            # print("No Match found")
            updated_links.update({x : temp_value[cnt]})
            cnt += 1
    # print(updated_links.items())
    return updated_links

def guilds_update(guild_id):
    with open('config.json', 'r') as f:
        data = json.load(f)
        friendlies = data["Friendlies"]
    for key,value in friendlies.items():
        if len(data[guild_id]) != len(friendlies):
            try:
                # tries to keep current data
                # if error then key does not exist so it goes to execption
                data[guild_id][key] = data[guild_id][key]
            except:
                # since key doesn't exist this adds the key with a blank value
                data[guild_id].update({key : {} })
    return data[guild_id]

# https://stackoverflow.com/questions/63369027/handling-errors-in-discord-py-no-permission
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You are missing permissions to run this command.")
    elif isinstance(error, CommandNotFound):
        await ctx.send("`Command Not Found.`")
    else:
        raise error

@bot.command()
async def ping(ctx):
    await ctx.send("Pong")

# @bot.command()
# async def help(ctx):
#     with open('config.json', 'r') as f:
#         config = json.load(f)
#         for i in config['cmds']:
#             print(i)

#Use The Token From Above to connect
bot.run(TOKEN)
