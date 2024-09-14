# How to use


## Create a new venv folder and open it 
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```

## Import all the needed modules
```
sudo .venv/bin/pip install 'discord.py[voice]' python-dotenv requests numerize Pillow colorlog

```

## Clone Altpapier's Github (only need to do this if you want to use specific emote Functions)
```
git clone https://github.com/Altpapier/Skyblock-Item-Emojis.git
```

## Create all needed environment variables
Create a file named .env in the root directory of your project and add the following keys to it

- HYPIXEL_API_TOKEN="" -> you can get this from https://developer.hypixel.net/
- DISCORD_API_TOKEN="" -> you can get this from https://discord.com/developers
- LOGGING_CHANNEL = "" -> rightclick on the channel you want the bot to send their logs to and "Copy Channel-ID"
