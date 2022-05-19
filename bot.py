from gettoken import *
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import MissingPermissions
from discord.ext.commands import CommandNotFound
import logging
from typing import Optional
from datetime import datetime, timedelta, time
import asyncio

days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]



logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = gettoken()
TOKEN = token["token"]

def get_prefix(client, message): 
    with open('config.json', 'r') as f: 
        prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]["prefix"] 
 
bot = commands.Bot(command_prefix= (get_prefix))

    


@bot.event
async def on_guild_join(guild): 
    prefix = 'bot!'
    chan_names = "Friendlies"
    channels = {}
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f'Hello, I\'m {bot.user}. Thanks for inviting me. \n'
                f'Use `{prefix}` for the start any of my commands.\n'
                f'Administrators can change this by using `{prefix}changeprefix "newPrefix"` command ')
        break
    with open('config.json', 'r') as f: 
        data = json.load(f) 
    
    channels.update({ "prefix" : prefix })
    temp = {}
    for i in data[chan_names]:
        temp.update({ i : data[chan_names][i]})
    channels.update({ "links" : temp })


    for i in data[chan_names]:
        channels.update({ i : {} })
    data[str(guild.id)] = channels

    with open('config.json', 'w') as f: 
        json.dump(data, f, indent=4) 




@bot.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('config.json', 'r') as f: #read the file
        data = json.load(f)
    data.pop(str(guild.id)) #find the guild.id that bot was removed from
    with open('config.json', 'w') as f: 
        json.dump(data, f, indent=4)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) 
async def changeprefix(ctx, prefix): 
    if ctx.message.author.guild_permissions.administrator:
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)]["prefix"] = prefix

        with open('config.json', 'w') as f: 
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to: {prefix}') 
    else:
        ctx.send(f'{ctx.message.author.mention} does not have permission for this command!')


@bot.command(aliases=["setrules", "setlink", "setlinks", "gamerule", "gamerules", "setdoc", "setdocs", "setdocument", "setdocuments"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def setrule(ctx, args1: Optional[str] = None):
    if ctx.message.author.guild_permissions.administrator:
        place = right_category(ctx)
        if place == False:
            return
        guild = ctx.message.guild
        chat_location = ctx.channel
        if args1 == None:
            args1 = ""
        cat_name = "Friendlies"
        with open('config.json', 'r') as f:
            data = json.load(f)
            data[str(guild.id)]["links"].update({chat_location.name : args1})
        with open('config.json', 'w') as f: 
            json.dump(data, f, indent=4)
    else:
        ctx.send(f'{ctx.message.author.mention} does not have permission for this command!')

@bot.command(aliases=["rule", "showrule", "showrules", "showlink", "showlinks", "showgamerule", "showgamerules", "showdoc", "showdocs", "showdocument", "showdocuments"])
async def rules(ctx):
    place = right_category(ctx)
    if place == False:
        return
    guild = ctx.message.guild
    chat_location = ctx.channel
    cat_name = "Friendlies"
    chat_name = ""
    with open('config.json', 'r') as f:
        data = json.load(f)
        rule = data[str(guild.id)]["links"][chat_location.name]
        for key,value in data["Names"].items():
            if key == chat_location.name:
                chat_name = value
    embed = discord.Embed(title=f'{chat_name}')
    embed.add_field(name="Rules", value=f'{rule}', inline = True)
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
    await chat_location.send(embed=embed)

@bot.event
async def on_message(msg):
    if bot.user.mentioned_in(msg):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)
            pre = prefixes[str(msg.guild.id)]["prefix"]
            await msg.channel.send(f'Your command prefix is: {pre}\n'
                f'You can type `{pre}help` for more help')
    await bot.process_commands(msg)

@bot.command(aliases=["jointeams","jointeam"])
async def join(ctx, args1: Optional[int] = None):
    place = right_category(ctx)
    if place == False:
        return
    guild = ctx.message.guild
    user_id = ctx.message.author.id
    user = await bot.fetch_user(user_id)
    cat_name = "Friendlies"
    cat_day = "Days"
    team_dict = {}
    if args1 == None:
        args1 = 1
    chat_location = None
    chat_day = None
    day_match = False
    guild_id = None
    weekday = datetime.weekday(datetime.now())
    now = datetime.now()
    with open('config.json', 'r') as f:
        config = json.load(f)
        for i in config[cat_name]:
            if i == str(ctx.channel):
                chat_location = ctx.channel
                break

        for i in config[cat_day]:
            if i == str(ctx.channel):
                print("Match Day in Json")
                chat_day = config[cat_day][i]
                print(chat_day)
                print(days[weekday])
                if days[weekday].lower() in chat_location.name.lower():
                    day_match = True
                    break
                day_match = False
                break
        
        if day_match != True:
            print(day_match)
            if str(chat_location.type) == 'text':
                for day in days:
                    if day.lower() in chat_location.name.lower():
                        print("-", day)
                        if days[weekday + 1].lower() in chat_location.name.lower():
                            print("Is one day early, checking is its after 12:00")
                            if time(datetime.now().hour) >= time(12):
                                print("It's noon or later.")
                                # it is after or is noon
                                continue
                            else:
                                await chat_location.send(f'{user.mention} it is too early to join {chat_location.name}.\nTry again later.')
                                return
                                # if it is after noon then continue witht the join
                        else:
                            await chat_location.send(f'{user.mention} it is too early to join {chat_location.name}.\nTry again later.')
                            return

        for x in config:
            if x == str(guild.id):
                guild_id = x
                break
        team_dict = config[guild_id][chat_location.name] 
        team_dict.update({user_id : args1})
        config[guild_id][chat_location.name] = team_dict
        with open('config.json', 'w') as f:
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
                if x == str(guild.id):
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
            with open('config.json', 'w') as f: 
                json.dump(config, f, indent=4)
            await chat_location.send(f'{user.mention} has left {chat_location.name} with `{all_teams}` teams.')
        else:
            print(config[guild_id][chat_location.name][str(user_id)])
            current_val = config[guild_id][chat_location.name][str(user_id)]
            if current_val < args1:
                all_teams = config[guild_id][chat_location.name][str(user_id)]
                with open('config.json', 'w') as f: 
                    json.dump(config, f, indent=4)
                await chat_location.send(f'{user.mention} has left {chat_location.name} with `{all_teams}` teams.')
            else:
                config[guild_id][chat_location.name].update({str(user_id) : current_val - args1})
                with open('config.json', 'w') as f: 
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

@bot.command(aliases=["listteams", "listteam", "listcoach", "listcoaches"])
async def list(ctx):
    place = right_category(ctx)
    if place == False:
        return
    guild = ctx.message.guild
    user_id = ctx.message.author.id
    chat_location = ctx.channel
    with open('config.json', 'r') as f:
        data = json.load(f)
    embed = discord.Embed(title=f'{chat_location.name}')
    cnt = 1
    coaches = []
    team_num = []
    for key,val in data[str(guild.id)][chat_location.name].items():
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

    embed.add_field(name = 'Coaches', 
        value= '\n'.join([f'{i}' for i in coaches]), 
        inline = True)
    white_space = '\x7f'
    embed.add_field(name = u'{0}'.format(white_space), 
        value= u'{0}'.format(white_space), 
        inline = True)
    
    embed.add_field(name = 'Number of Teams', 
        value= '\n'.join([f'{x}' for x in team_num]), 
        inline = True)


    await chat_location.send(embed=embed)

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
        with open('config.json', 'r') as f:
            data = json.load(f)
        teams = sort_teams(guild, chat_location)
        if len(teams) <= 1:
            if len(teams) == 0:
                await chat_location.send("`No coaches joined to create a match.`")
                return
            await chat_location.send("`Not enough coaches to create match.`")
            return
        firstkey = next(iter(teams))
        firstval = teams[firstkey]
        print(firstkey, ":" , firstval)

        teams.pop(firstkey)

        secondkey = next(iter(teams))
        secondval = teams[secondkey]
        print(secondkey, ":" , secondval)

        teams.pop(secondkey)
        true = True
        while true:
            left = match_teams(firstkey, firstval, secondkey, secondval)
            temp_secondkey = next(iter(left))
            temp_secondval = left[temp_secondkey]
            if temp_secondval == 0:
                print("inside temp_secondval == 0")
                coach1 = await bot.fetch_user(int(firstkey))
                coach2 = await bot.fetch_user(int(secondkey))
                await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                            f'`Away:` {coach2.mention}\n'
                                            f'`Setup {secondval} matche(s).\n`'
                                            "GLHF!")
                if len(teams) == 1:
                    msgKey = next(iter(teams))
                    coach1 = await bot.fetch_user(int(msgKey))
                    msgValue = teams[msgKey]
                    await chat_location.send('!!Attention!!\n'
                                            f'{coaches_role.mention}\n'
                                            f'{coach1.mention} needs {msgValue} matche(s).')
                    true = False
                    break
                elif  len(teams) == 0:
                    print("no teams left, printing msg about matches")
                    coach1 = await bot.fetch_user(int(firstkey))
                    coach2 = await bot.fetch_user(int(secondkey))
                    await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                                f'`Away:` {coach2.mention}\n'
                                                f'`Setup {secondval} matche(s).\n`'
                                                "GLHF!")
                    true = False
                    break
                firstkey = next(iter(teams))
                firstval = teams[firstkey]
                print(firstkey, ":" , firstval)
                teams.pop(firstkey)
                secondkey = next(iter(teams))
                secondval = teams[secondkey]
                print(secondkey, ":" , secondval)
                teams.pop(secondkey)
            elif temp_secondval > 0:
                print("inside temp_secondval > 0")
                coach1 = await bot.fetch_user(int(firstkey))
                coach2 = await bot.fetch_user(int(secondkey))
                await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                            f'`Away:` {coach2.mention}\n'
                                            f'`Setup {secondval} matche(s).\n`'
                                            "GLHF!")
                if len(teams) == 0:
                    coach2 = await bot.fetch_user(int(firstkey))
                    await chat_location.send('!!Attention!!\n'
                                            f'{coaches_role.mention}\n'
                                            f'{coach2.mention} needs {temp_secondval} matche(s).')
                    true = False
                    break
                print("had reminder teams in json")
                firstkey = next(iter(teams))
                firstval = teams[firstkey]
                print(firstkey, ":" , firstval)
                teams.pop(firstkey)
                secondkey = temp_secondkey
                secondval = temp_secondval
            else:
                print("Should not be here!")
        data[str(guild.id)].update({chat_location.name : {} })
        with open('config.json', 'w') as f: 
            json.dump(data, f, indent=4) 
        print(f"all data from {chat_location.name} has been cleared")
    else:
        ctx.send(f'{ctx.message.author.mention} does not have permission for this command!')

@commands.command()
async def bot_match(day):
    for guild in bot.guilds:
        for channel in guild.channels:
            if str(channel.type) == 'text':
                if days[day].lower() in channel.name.lower():
                    print ("Found channel", channel.name.lower())
                    chat_location = channel
                    teams = {}
                    role_name = "Coaches"
                    coaches_role = discord.utils.get(guild.roles,name=role_name)
                    with open('config.json', 'r') as f:
                        data = json.load(f)
                    teams = sort_teams(guild, chat_location)
                    if len(teams) <= 1:
                        if len(teams) == 0:
                            await chat_location.send("`No coaches joined to create a match.`")
                            return
                        await chat_location.send("`Not enough coaches to create match.`")
                        return
                    firstkey = next(iter(teams))
                    firstval = teams[firstkey]
                    print(firstkey, ":" , firstval)

                    teams.pop(firstkey)

                    secondkey = next(iter(teams))
                    secondval = teams[secondkey]
                    print(secondkey, ":" , secondval)

                    teams.pop(secondkey)
                    true = True
                    while true:
                        left = match_teams(firstkey, firstval, secondkey, secondval)
                        temp_secondkey = next(iter(left))
                        temp_secondval = left[temp_secondkey]
                        if temp_secondval == 0:
                            print("inside temp_secondval == 0")
                            coach1 = await bot.fetch_user(int(firstkey))
                            coach2 = await bot.fetch_user(int(secondkey))
                            await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                                        f'`Away:` {coach2.mention}\n'
                                                        f'`Setup {secondval} matche(s).\n`'
                                                        "GLHF!")
                            if len(teams) == 1:
                                msgKey = next(iter(teams))
                                coach1 = await bot.fetch_user(int(msgKey))
                                msgValue = teams[msgKey]
                                await chat_location.send('!!Attention!!\n'
                                                        f'{coaches_role.mention}\n'
                                                        f'{coach1.mention} needs {msgValue} of matche(s).')
                                true = False
                                break
                            elif  len(teams) == 0:
                                print("no teams left, printing msg about matches")
                                coach1 = await bot.fetch_user(int(firstkey))
                                coach2 = await bot.fetch_user(int(secondkey))
                                await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                                            f'`Away:` {coach2.mention}\n'
                                                            f'`Setup {secondval} matche(s).\n`'
                                                            "GLHF!")
                                true = False
                                break
                            firstkey = next(iter(teams))
                            firstval = teams[firstkey]
                            print(firstkey, ":" , firstval)
                            teams.pop(firstkey)
                            secondkey = next(iter(teams))
                            secondval = teams[secondkey]
                            print(secondkey, ":" , secondval)
                            teams.pop(secondkey)
                        elif temp_secondval > 0:
                            print("inside temp_secondval > 0")
                            coach1 = await bot.fetch_user(int(firstkey))
                            coach2 = await bot.fetch_user(int(secondkey))
                            await chat_location.send(   f'`Home:` {coach1.mention}\n' 
                                                        f'`Away:` {coach2.mention}\n'
                                                        f'`Setup {secondval} matche(s).\n`'
                                                        "GLHF!")
                            if len(teams) == 0:
                                coach2 = await bot.fetch_user(int(firstkey))
                                await chat_location.send('!!Attention!!\n'
                                                        f'{coaches_role.mention}\n'
                                                        f'{coach2.mention} needs {temp_secondval} of matche(s).')
                                true = False
                                break
                            print("had reminder teams in json")
                            firstkey = next(iter(teams))
                            firstval = teams[firstkey]
                            print(firstkey, ":" , firstval)
                            teams.pop(firstkey)
                            secondkey = temp_secondkey
                            secondval = temp_secondval
                        else:
                            print("Should not be here!")
                    data[str(guild.id)].update({chat_location.name : {} })
                    with open('config.json', 'w') as f: 
                        json.dump(data, f, indent=4) 
                    print(f"all data from {chat_location.name} has been cleared")



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
        print(e)
    print(temp)
    return temp

def sort_teams(guild, channel):
    temp = {}
    with open('config.json', 'r') as f:
        data = json.load(f)
    temp = dict(sorted(data[str(guild.id)][channel.name].items(), key=lambda item: item[1], reverse=True))
    return temp

def right_category(ctx):
    guild = ctx.message.guild
    cat_name = "Friendlies"
    category = discord.utils.get(guild.categories, name=cat_name)
    if str(category) != cat_name:
        return False
    return True

@bot.command(aliases=["setup", "createchannels", "makechannels"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def setupchannels(ctx):
    if ctx.message.author.guild_permissions.administrator:
        guild = ctx.message.guild
        message = ""
        cat_name = "Friendlies"
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
            pass
        with open('config.json', 'r') as f:
            config = json.load(f)
            message += "Channels Created: \n`"
            category = discord.utils.get(guild.categories, name=cat_name)
            print(category)
            cnt = 0
            for i in config[cat_name]:
                try:
                    channel = discord.utils.get(guild.text_channels, name=i)
                    if channel == None:
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

def get_text_channels(guild):
    text_channel_list = []
    for channel in guild.text_channels:
        text_channel_list.append(channel.name)
    return text_channel_list


@bot.event
async def on_ready():
    print(
        f'{bot.user} is online.\n'
    )
    print("Starting Task: task_match_coaches.start()")
    task_match_coaches.start()
    print("Starting Task: task_announce_open.start()")
    task_announce_open.start()
    
@bot.command(aliases=["listguilds","guildslist","showallguilds"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def showguilds(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if ctx.author.id != 225769313183727617:
            return
        message = ""
        num = 1
        for guild in bot.guilds:
            message += f"{num}.{guild.name}  - ID: {guild.id}\n"
            num = num + 1
        await ctx.send(message)
    else:
         ctx.send(f'{ctx.message.author.mention} does not have permission for that command.')

@bot.command(aliases=["updateconf","confupdate","configupdate"])
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def updateconfig(ctx):
    if ctx.message.author.guild_permissions.administrator:
        message = ""
        num = 1
        
        with open('config.json', 'r') as f:
            data = json.load(f)
            temp_prefix = ""
            temp_links = {}
            temp_friendlies = {}
        for guild in bot.guilds:
            for key,value in data[str(guild.id)].items():
                if key == "prefix":
                    temp_prefix = data[str(guild.id)]["prefix"]
                    pass
                if key == "links":
                    temp_links = links_update(str(guild.id))
                    pass
            
            data[str(guild.id)].pop("prefix")
            data[str(guild.id)].pop("links")
            temp_friendlies = guilds_update(str(guild.id))
            data.pop(str(guild.id))
            data.update({str(guild.id): {}})
            data[str(guild.id)]["prefix"] = temp_prefix
            data[str(guild.id)]["links"] = temp_links
            data[str(guild.id)] = temp_friendlies
            message += f"{num}.{guild.name} = Updated Config\n"
            num = num + 1
        await ctx.send(message)
        with open('config.json', 'w') as f: 
            json.dump(data, f, indent=4) 
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
    cnt = 0
    for x in temp_key:
        try:
            temp_key2.index(x)
            updated_links.update({temp_key2[cnt] : temp_value2[cnt]})
            cnt += 1
        except:
            updated_links.update({x : temp_value[cnt]})
            cnt += 1
    return updated_links

def guilds_update(guild_id):
    with open('config.json', 'r') as f:
        data = json.load(f)
        friendlies = data["Friendlies"]
    for key,value in friendlies.items():
        if len(data[guild_id]) != len(friendlies):
            try:
                data[guild_id][key] = data[guild_id][key]
            except:
                data[guild_id].update({key : {} })
    return data[guild_id]

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You are missing permissions to run this command.")
    elif isinstance(error, CommandNotFound):
        await ctx.send("`Command Not Found.`")
    else:
        raise error



def seconds_until(hours, minutes):
    given_time = time(hours, minutes)
    now = datetime.now()
    future_exec = datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  
        future_exec = datetime.combine(now + timedelta(days=1), given_time) 
    return (future_exec - now).total_seconds()
    
@tasks.loop(minutes=60.0)
async def task_match_coaches():
    # use miltary time
    hour = 14
    minutes = 30
    if datetime.now().hour == hour:
        print (seconds_until(hour, minutes))
        await asyncio.sleep(seconds_until(hour, minutes))
        weekday = datetime.weekday(datetime.now())
        if weekday == 0: #Monday
            print("Monday")
            await bot_match(weekday)
            #[Do your stuff]
        if weekday == 1: #Tuseday
            print("tuseday")
            await bot_match(weekday)
            #[Do your stuff]
        if weekday == 2: #Wednesday
            print("wednesday")
            await bot_match(weekday)
            #[Do your stuff]
        if weekday == 3: #Thursday
            print("thursday")
            await bot_match(weekday)
            #[Do your stuff]
        if weekday == 4: #Friday
            print("friday")
            await bot_match(weekday)
            #[Do your stuff]
        await asyncio.sleep(60)

@commands.command()
async def anounceOpen(day):
     for guild in bot.guilds:
        for channel in guild.channels:
            if str(channel.type) == 'text':
                if day == 6: day = (-1)
                if days[day+1].lower() in channel.name.lower():
                    role_name = "Coaches"
                    coaches_role = discord.utils.get(guild.roles,name=role_name)
                    await channel.send(f'{coaches_role.mention}\n'
                                        f'Teams are now able to join {channel.name}')

@tasks.loop(minutes=60.0)
async def task_announce_open():
    # use miltary time
    hour = 12
    minutes = 30
    if datetime.now().hour == hour:
        print (seconds_until(hour, minutes))
        await asyncio.sleep(seconds_until(hour, minutes))
        weekday = datetime.weekday(datetime.now())
        if weekday == 0: #Monday
            print("Monday")
            await anounceOpen(weekday)
            #[Do your stuff]
        if weekday == 1: #Tuseday
            print("tuseday")
            await anounceOpen(weekday)
            #[Do your stuff]
        if weekday == 2: #Wednesday
            print("wednesday")
            await anounceOpen(weekday)
            #[Do your stuff]
        if weekday == 3: #Thursday
            print("thursday")
            await anounceOpen(weekday)
            #[Do your stuff]
        if weekday == 4: #Friday
            print("friday")
            await anounceOpen(weekday)
            #[Do your stuff]
        await asyncio.sleep(60)

# https://stackoverflow.com/questions/43465082/python-discord-py-delete-all-messages-in-a-text-channel
@bot.command(pass_context = True, name='clear', help='this command will clear msgs')
@commands.has_permissions(administrator=True) 
async def clear(ctx, number: Optional[int] = 5):
    if ctx.message.author.guild_permissions.administrator:
        if number >= 100: number = 99
        try:
            await ctx.channel.purge(limit=number)
        except:
            print("An exception occurred while deleting msgs.\n")

@bot.command()
async def ping(ctx):
    print ("Recived: Ping")
    print ("Sending: Pong")
    await ctx.send("Pong")

#Use The Token From Above to connect
bot.run(TOKEN)
