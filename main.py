import discord
import asyncio
import datetime
import requests
import json
from discord.ext import commands, tasks


# Get today's Holidays
def get_holidays():
      # Get the list of holidays
    holidays = []
    date = datetime.datetime.now()
    today = f"{date.month}/{date.day}/{date.year}"

    response = requests.get(f"https://www.checkiday.com/api/3/?d={today}")
    holidays_list = json.loads(response.content)["holidays"]
    
    for i in range(len(holidays_list)):
        holiday = holidays_list[i]
        holidays.append(holiday["name"])

    holidays = "\n".join(holidays)
    return holidays

# Discord Bot
bot = commands.Bot(command_prefix="!checkiday ")
channel_list = {}

# Sets value in json to guild id upon the bot joining the guild
@bot.event
async def on_guild_join(guild):
    #loads json file to dictionary
    with open("db.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[guild.id] = guild.text_channels[0] #sets key to guilds id and value to top textchannel
    
    #writes dictionary to json file
    with open("db.json", "w") as f:
        json.dump(guildInfo, f)


# Commands

@bot.command()
async def channelid(ctx, arg):
    with open("db.json", "r") as f:
        guildInfo = json.load(f)
    guildInfo[ctx.message.guild.id] = arg
    with open("db.json", "w") as f:
        json.dump(guildInfo, f)



@tasks.loop(seconds=30)
async def called_once_a_day():
   
    holidays = get_holidays()
    # Send the message
    with open("db.json", "r") as f:
        guildInfo = json.load(f)

    for i in guildInfo:
        channel = bot.get_channel(int(guildInfo[i]))
        try:
            print("------------")
            print(f"channel: {channel}")
            print(f"guildInfo[i]: {guildInfo[i]}")
            await channel.send(f"__Today's Holidays__\n\n{holidays}")
        except: print("error!")


@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

called_once_a_day.start()




# Read Token
f = open("secrets.txt")
token = f.readline().rstrip()
f.close


bot.run(token)