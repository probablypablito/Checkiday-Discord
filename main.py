import discord
import datetime
import requests

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

reponse = requests.get(f"https://www.checkiday.com/api/3/?d={today}")

print(reponse.content)


#client.run(token)

