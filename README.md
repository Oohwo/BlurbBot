# BlurbBot
-----
Basically Blurbot but with slash commands and cleaner code!
-----
## Demo

![Demo](https://cdn.discordapp.com/attachments/1030373948694728764/1033689034742046820/Testing_BlurbBot.gif)

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
