# Checkiday-Discord
 A Discord bot to tell you the current holidays

# To use
Use `/holidays` to get today's holidays

Use `/setchannel` to set the daily (17:00 UTC) holiday notifications to the current channel

## Docker
1) Create a volume `sudo docker volume create checkiday-discord`
2) Run the docker image with `sudo docker run --name checkiday-discord -e TOKEN=<token.goes.here> -d -v checkiday-discord:/app/db probablypablito/checkiday-discord`