import datetime, requests
import json, random
import discord
from discord.ext import tasks
import os

def today(type):
    date = datetime.datetime.now()
    if (type == "date"):
        today = f"{date.month}/{date.day}/{date.year}"   
    elif (type == "unix"):
        today = date.timestamp()
        today = round(today)
    return today



# Get today's Holidays
def get_holidays(type="none"):
    # Get the list of holidays
    holidays = []
    
    todays_date = today("date")
    response = requests.get(f"https://www.checkiday.com/api/3/?d={todays_date}")
    holidays_list = json.loads(response.content)["holidays"]
    
    for i in range(len(holidays_list)):
        holiday = holidays_list[i]
        holidays.append(holiday["name"])
    if (type == "list"): 
        return holidays
    holidays = "\n".join(holidays)
    return holidays

# Get random Holiday for Status
def rand_holiday():
    todays_holidays = get_holidays("list")
    rand_number = random.randint(0,len(todays_holidays)-1)
    rand_holiday = todays_holidays[rand_number]
    return rand_holiday

# Setup the bot
random_holiday = rand_holiday()
bot = discord.Bot(activity=discord.Game(name=random_holiday))

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Commands
@bot.slash_command()
async def setchannel(ctx):
    with open("db.json", "r") as f:
        guildInfo = json.load(f)
        guildInfo[ctx.guild.id] = ctx.channel.id
    with open("db.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.respond(f"Set channel to <#{ctx.channel.id}>")

@bot.slash_command()
async def holidays(ctx):
    holidays = get_holidays()
    todays_date = today("unix")
    await ctx.respond(f"**__Holidays for <t:{todays_date}:D>__**\n\n{holidays}")





# Loop every 24h
@tasks.loop(hours=24)
async def called_once_a_day():
    # Change Status
    random_holiday = rand_holiday()
    await bot.change_presence(activity=discord.Streaming(name=random_holiday, url="https://twitch.tv/probablypablito"))
   
    holidays = get_holidays()

    # Send the message with Holiday list
    with open("db.json", "r") as f:
        guildInfo = json.load(f)

    for i in guildInfo:
        channel = bot.get_channel(int(guildInfo[i]))
        try:
            print("------------")
            print(f"channel: {channel}")
            print(f"guildInfo[i]: {guildInfo[i]}")
            todays_date = today("unix")
            await channel.send(f"**__Holidays for <t:{todays_date}:D>__**\n\n{holidays}")
        except: print("error!")

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

called_once_a_day.start()

# Run the bot
bot.run(os.getenv("TOKEN"))