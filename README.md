# BlurbBot
-----
*Blurb Bot* is a Discord bot written in Python to keep track of my rants, quotes, and other miscellaneous life stuff!

This is the newer version of [*Blurbot*](https://github.com/Oohwo/Blurbot) and includes slash commands from Discord.py 2.0.

I wrote this because I don't want to burden my friends with rambling my mouth off, and it's a cool first Discord bot :)

The bot is currently being hosted on [railway.app](https://railway.app) and I'm using Airtable to store all my data. 

At the moment, I am only sending invite links to close friends (on request)! This bot is meant as a personal journaling bot for myself as well as a way to teach my friends how to create their own Discord bots. Feel free to fork and host this bot on your own as an example :)

## Demo

![Demo](https://cdn.discordapp.com/attachments/1030373948694728764/1033689034742046820/Testing_BlurbBot.gif)

## Current Features
`/new_quote` - Shows all commands

`/rant` - Tell Blurb how you're feeling

Other stuff:
- When someone says "Hello there.", the bot says "General Kenobi."
- Reacting to a message with :flushed: prompts the bot to say :flushed:

## Installation
1. Download this repo
2. Navigate to the bot directory via Terminal
3. Create a virtual environment: 
- Mac: `python3 -m venv bot-env`
- Windows: `py -3 -m venv bot-env` 
4. Activate the virtual environment: 
- Mac: `source bot-env/bin/activate`
- Windows: `bot-env\Scripts\activate.bat`
5. Install the needed libraries: 
- Mac: `pip install -r requirements.txt`
- Windows: `py -3 -m pip install -r requirements.txt`
6. Create a `.env` file with:
- `DISCORD_BOT_TOKEN = ''`
- `DISCORD_BOT_APP_ID = ''`
- `AIRTABLE_API_KEY = ''`
- `AIRTABLE_BASE_ID = ''`
7. Run `main.py`

## Notes
Airtable functions may not work!
