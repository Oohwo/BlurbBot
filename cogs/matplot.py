import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import discord
from discord.ext import commands
from discord import app_commands

class Matplot(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name='matplot_test', description='im testing again lol')
  async def button_test(self, interaction: discord.Interaction):
    xkcd_matplot()
    plot_file = discord.File(fp='./cogs/plots/xkcd_plot.png')
    await interaction.response.send_message(file=plot_file)

def xkcd_matplot():
  with plt.xkcd():
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.title('this is a test')
    plt.xlabel('im an x axis')
    plt.ylabel('im a y axis')
    plt.savefig('./cogs/plots/xkcd_plot.png', transparent = True)

async def setup(bot: commands.Bot):
  '''adds cog to bot'''
  await bot.add_cog(Matplot(bot))