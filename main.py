import discord
import asyncio
import datetime
import requests
import json
from discord.ext import commands, tasks


# Discord Bot
bot = commands.Bot(command_prefix="!checkiday ")

# Commands

@bot.command()
async def channelid(ctx, arg):
    global channel_id
    channel_id = int(arg)
    await ctx.send(f"Set channel id to {arg}")




@tasks.loop(seconds=30)
async def called_once_a_day():
    message_channel = bot.get_channel(channel_id)
    print(f"Got channel {message_channel}")
    
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
   # print(holidays)
    if (channel_id):
        await message_channel.send(f"__Today's Holidays__\n\n{holidays}")

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