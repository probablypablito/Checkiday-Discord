import datetime, requests
import json, random
import discord
from discord.ext import tasks
import os
from discord.utils import get


def today(type):
    date = datetime.datetime.now()
    if (type == "date"):
        today = f"{date.month}/{date.day}/{date.year}"   
    elif (type == "word"):
        today = date.strftime("%B %m %Y")
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
    if not os.path.exists('db/db2.json'):
        with open("db/db.json", "a") as f:
            f.write("{}")
            f.close
    with open("db/db.json", "r") as f:
        guildInfo = json.load(f)
        guildInfo[str(ctx.guild.id)] = str(ctx.channel.id)
    with open("db/db.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.respond(f"Set channel to <#{ctx.channel.id}>")

@bot.slash_command()
async def holidays(ctx):
    holidays = get_holidays()
    todays_date = today("word")
    await ctx.respond(f"**__Holidays for {todays_date}__**\n{holidays}")

@tasks.loop(minutes=1)
async def send_holidays():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    

    if(current_time != '17:00'):  # check if matches with the desired time
        return

    # Change Status
    random_holiday = rand_holiday()
    await bot.change_presence(game=discord.Game(name=random_holiday, type=1))
   
    holidays = get_holidays()

    # Send the message with Holiday list
    with open("db/db.json", "r") as f:
        guildInfo = json.load(f)

    for i in guildInfo:
        channel = bot.get_channel(int(guildInfo[i]))
        guild = bot.get_guild(int(i))

        try:
            todays_date = today("word")
            role = get(guild.roles, name="Holidays")
            if role == None:
                role = get(guild.roles, name="holidays") # Try to check if it's all lowercase
            await channel.send(f"**__{role.mention} for {todays_date}__**\n{holidays}")
        except: print("error sending holiday list")



@send_holidays.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


send_holidays.start()
bot.run(os.getenv("TOKEN"))