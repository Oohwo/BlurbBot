import asyncio
from venv import create
import discord
import os
from pytz import timezone
from pyairtable import Table
import random
from datetime import datetime
from discord.ext import commands
from discord import app_commands
import pandas as pd

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_QUOTEBOOK_BASE_ID')
tz = timezone('US/Eastern')

class Quotebook(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name='new_quote', description='Create a new quote!')
  async def new_quote(self, interaction: discord.Interaction, quote: str, author: str, context: str) -> None:
    '''/new_quote [quote] [author] [context] - saves new quote into Airtable'''
    table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, 'Quotebook')

    timestamp=datetime.now(tz)
    success = await upload_to_airtable(table, [author, str(timestamp), quote, context])
    if success:
      quote_summary = f'\"*{quote}*\" - {author}' # TODO: create embed
      await interaction.channel.send(quote_summary)
      await interaction.response.send_message('Quote successfully saved to Airtable!', ephemeral=True)
    else:
      await interaction.response.send_message('Quote failed to save to Airtable!', ephemeral=True)

  @app_commands.command(name='rant', description='Rant to the bot!')
  async def rant(self, interaction: discord.Interaction) -> None:
    '''/rant - creates a thread that the user can rant in... saves rant to Airtable'''
    rant_timestamp = datetime.now(tz)
    rant_timestamp_str = rant_timestamp.strftime("%m᜵%d᜵%y - %I.%M %p")
    rant_msg = ''
    emoji = '💭'

    table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, 'Rants')
    thread = await interaction.channel.create_thread(name=f'{rant_timestamp_str}', type=discord.ChannelType.public_thread)
    await interaction.response.send_message('Thread created!', ephemeral=True)
    await prompt_wait(thread)
    await thread.send("Hey! Release all your thoughts to me until you say you're 'done'. I don't mind. :)")

    def check(m):
      return m.author == interaction.user and m.channel
    
    reply = await self.bot.wait_for('message', check=check)
    rant_msg = reply.content
    
    while reply.content != 'done':
      await reply.add_reaction(emoji)
      reply = await self.bot.wait_for('message', check=check)
      if reply.content == 'done':
        done = '🤐'
        await reply.add_reaction(done)
      else:
        rant_msg = f'{rant_msg}\n{reply.content}'
    
    table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, 'Rants')

    success = await upload_to_airtable(table, [str(rant_timestamp), rant_msg])
    if success:
      await prompt_wait(thread)
      await thread.send(f'Hey, I wrote your rant up onto the cloud so you can look back on it later.')
      await prompt_wait(thread)
      await thread.send(f'Always here to chat if you need to. <3')
    else:
      await thread.send(f'Rant failed to save to Airtable... please try again.')

async def upload_to_airtable(airtable, fields):
  '''creates a record out of the fields, attempts to append record into airtable, returns a boolean'''
  try:
    airtable_df = pd.DataFrame(airtable.all())
    airtable_col_names = list(airtable_df['fields'][0].keys())
    record_dict = dict(zip(airtable_col_names, fields))
    airtable.create(record_dict)
    return True
  except:
    return False

async def prompt_wait(channel):
  '''shows lifelike typing in specified channel'''
  async with channel.typing():
    type_time = random.uniform(2.5, 3)
    await asyncio.sleep(type_time)

async def create_thread(name, channel):
  '''creates a thread in [channel] called [name]'''
  return await channel.create_thread(name=name, type=discord.ChannelType.public_thread)

async def setup(bot: commands.Bot):
  '''adds cog to bot'''
  await bot.add_cog(Quotebook(bot))