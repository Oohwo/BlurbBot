import asyncio
from email import message
from email.mime import image
from venv import create
import discord
import os
from pyairtable import Table
import random
from discord.ext import commands
from discord import app_commands
import pandas as pd

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_HANGMAN_BASE_ID')

class Hangman(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name='hangman', description='Play Hangman!')
  async def play_hangman(self, interaction: discord.Interaction) -> None:
    secret_word = generate_secret_word()
    embed = await HangmanEmbed(secret_word).generate_embed()
    embed.set_image(url="https://cdn.discordapp.com/attachments/1030374642654920755/1034006440064581642/creeper_0.png")
    await interaction.response.send_message(embed=embed)

    def check(m):
      return m.author == interaction.user and m.channel

    reply = await self.bot.wait_for('message', check=check)
    embed.description = f'`{secret_word}`\n\nLetters guessed so far:'

class HangmanEmbed():
  def __init__(self, secret_word, guess_list=[]) -> None:
    self.secret_word = secret_word
    self.guess_list = guess_list
    self.correct_guesses = []
    self.incorrect_guesses = []
    # self.correct_guesses, self.incorrect_guesses = self.generate_correct_incorrect()
    self.clue = str(self.regenerate_clue())
  
  async def generate_embed(self):
    return discord.Embed(title="Play Hangman!", 
    description=f'`{self.clue}`\n\nLetters guessed so far: {self.guess_list}\n\nThe secret word is `{self.secret_word}`', color=0x00aaff)

  async def set_embed_img(self):
    print('hi')

  def regenerate_clue(self):
    temp_clue = '_' * len(self.secret_word)
    for i in range(len(self.secret_word)):
      if self.secret_word[i] in self.correct_guesses:
        temp_clue = clue[:i] + self.secret_word[i] + clue[i+1:]
    
    clue = ''
    for i in range(len(temp_clue) - 1):
      clue = clue + temp_clue[i] + ' '
    clue = clue + temp_clue[-1]
    return clue
  
  def generate_correct_incorrect(self):
    correct_guesses, incorrect_guesses = []
    for i in self.guess_list:
      if i in self.secret_word:
        correct_guesses.append(i)
      else:
        incorrect_guesses.append(i)
    self.correct_guesses = correct_guesses
    self.incorrect_guesses = incorrect_guesses

async def setup(bot: commands.Bot):
  '''adds cog to bot'''
  await bot.add_cog(Hangman(bot))

def generate_secret_word():
  table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, 'Minecraft')
  airtable_df = pd.DataFrame(table.all())
  word_list = [record['word'] for record in airtable_df['fields']]
  wordIndex = random.randint(0, len(word_list) - 1)
  return word_list[wordIndex]