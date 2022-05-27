import discord
import datetime
import requests
import json

date = datetime.datetime.now()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()

# Read Token
f = open("secrets.txt")
token = f.readline().rstrip()
f.close

today = f"{date.month}/{date.day}/{date.year}"
print("today is: " + today)

response = requests.get(f"https://www.checkiday.com/api/3/?d={today}")


holidays_list = json.loads(response.content)["holidays"]


for i in range(len(holidays_list)):
    holiday = holidays_list[i]
    print(holiday["name"])
#client.run(token)