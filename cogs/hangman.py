import discord
import os
from pyairtable import Table
import random
from discord.ext import commands
from discord import app_commands
import pandas as pd
import string

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_HANGMAN_BASE_ID')

urls = os.environ.get('CREEPER_IMG_URLS')

class Hangman(commands.Cog):
  
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.secret_word = ''
    self.clue = ''
    self.num_incorrect = -1
    self.thread = None

    self.guesses = []
    self.incorrect_guesses = []
    self.correct_guesses = []

    self.embed = None

  @app_commands.command(name='hangman', description='Play Hangman!')
  async def play_hangman(self, interaction: discord.Interaction) -> None:

    async def get_guess():
      def check(m):
        return m.author == interaction.user and m.channel

      reply = await self.bot.wait_for('message', check=check)
      print(f'{reply.author} guessed: {reply.content}')
      if reply.content.lower() not in string.ascii_lowercase:
        await reply.channel.send(f'`{reply.content}` is not a letter, try again.')
        return await get_guess()
      elif reply.content in self.guesses:
        await reply.channel.send(f'`{reply.content}` has already been guessed, try again')
        return await get_guess()
      else:
        self.guesses.append(reply.content)
        return reply.content

    def regenerate_clue():
      temp_clue = '_' * len(self.secret_word)
      for i in range(len(self.secret_word)):
        if self.secret_word[i] in self.correct_guesses:
          temp_clue = temp_clue[:i] + self.secret_word[i] + temp_clue[i+1:]
      
      clue = ''
      for i in range(len(temp_clue) - 1):
        clue = clue + temp_clue[i] + ' '
      clue = clue + temp_clue[-1]
      return clue

    async def check_guess(guess):
      if guess in self.secret_word:
        await self.thread.send(f"`{guess}` is in the secret word!")
        return True
      await self.thread.send(f"Sorry, `{guess}` is not in the secret word.")
      return False

    async def generate_embed():
      return discord.Embed(title="Play Hangman!", 
      description=f'`{self.clue}`\n\nLetters guessed so far: {self.guesses}\n\nThe secret word is `{self.secret_word}`', color=0x00aaff)
    
    async def take_guesses():
      guess = await get_guess()
      if not await check_guess(guess):
        self.incorrect_guesses.append(guess)
        self.num_incorrect += 1
      else:
        self.correct_guesses.append(guess)
      self.clue = regenerate_clue()
      print(self.clue, self.num_incorrect)

    async def update_embed():
      self.embed = discord.Embed(title="Play Hangman!", 
      description=f'`{self.clue}`\n\nLetters guessed so far: {self.guesses}\n\nThe secret word is `{self.secret_word}`', color=0x00aaff)
      if self.num_incorrect > -1:
        self.embed.set_image(url=urls[self.num_incorrect])
      await interaction.edit_original_response(embed=self.embed)

    # async def reset():
    #   self.secret_word = ''
    #   self.clue = ''
    #   self.num_incorrect = -1
    #   self.thread = None

    #   self.guesses = []
    #   self.incorrect_guesses = []
    #   self.correct_guesses = []

    #   self.embed = None
    #   await update_embed()
    
    self.secret_word = generate_secret_word()
    self.clue = regenerate_clue()
    self.embed = await generate_embed()
    
    await interaction.response.send_message(embed=self.embed)
    self.thread = await interaction.channel.create_thread(name=f'Hangman', type=discord.ChannelType.public_thread)
    await self.thread.send('Hangman Thread created! Input your guesses here.')
    while self.num_incorrect < 6:
      await take_guesses()
      await update_embed()

async def setup(bot: commands.Bot):
  '''adds cog to bot'''
  await bot.add_cog(Hangman(bot))

def generate_secret_word():
  table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, 'Minecraft')
  airtable_df = pd.DataFrame(table.all())
  word_list = [record['word'] for record in airtable_df['fields']]
  wordIndex = random.randint(0, len(word_list) - 1)
  return word_list[wordIndex]