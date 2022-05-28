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
channel_id = 0

# Commands

@bot.command()
async def channelid(ctx, arg):
    global channel_id
    channel_id = int(arg)
    await ctx.send(f"Set channel to <#{arg}>")
    print(channel_id)



@tasks.loop(seconds=30)
async def called_once_a_day():
    if bot.get_channel(channel_id) == None: return 
    
    message_channel = bot.get_channel(channel_id)
    print(f"Got channel {message_channel}")
    holidays = get_holidays()
    # Send the message
    try:
        await message_channel.send(f"__Today's Holidays__\n\n{holidays}")
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












today = f"{date.month}/{date.day}/{date.year}"
response = requests.get(f"https://www.checkiday.com/api/3/?d={today}")
holidays_list = json.loads(response.content)["holidays"]

for i in range(len(holidays_list)):
    holiday = holidays_list[i]
    print(holiday["name"])