# Checkiday-Discord
 A Discord bot to tell you the current holidays

# To use

[Invite](https://discord.com/api/oauth2/authorize?client_id=979814139469893812&permissions=2147485696&scope=bot%20applications.commands) the bot to your server.

Use `/holidays` to get today's holidays

Use `/setchannel` to set the daily holiday notifications to the current channel

There is no permissions system on this bot, I just made this for fun.



# Self hosting for those that care:

## With Docker
1) Clone the repo & cd into it
2) Build the docker image with `sudo docker build --tag checkiday-discord .`
3) Make a folder somewhere with 1 file in called `db.json`. Inside put `{}`
4) Run the docker image with `sudo docker run -e TOKEN=<token.goes.here> -d -v /path/to/folder/:/app/db checkiday-discord`

## Without docker
1) Clone the repo & cd into it
2) Make a folder called `db` with 1 file in called `db.json`. Inside put `{}`
3) Make an enviornment variable called `TOKEN` and have it be your token
4) Alternatively insert your token manually into `main.py` at the bottom
5) Run `main.py`
