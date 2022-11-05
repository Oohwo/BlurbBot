import discord
from discord.ext import commands
from discord import app_commands

click_counter = 0

class TestingButtons(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name='button_test', description='im testing lol')
  async def button_test(self, interaction: discord.Interaction):
    global click_counter
    await interaction.response.send_message(f"You clicked me {click_counter} times! :O", view = button_view())
  
async def setup(bot: commands.Bot):
  '''adds cog to bot'''
  await bot.add_cog(TestingButtons(bot))

class button_view(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  
  @discord.ui.button(label = "Click Me!!!!", style = discord.ButtonStyle.green, custom_id = "what even is this")
  async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
    global click_counter
    click_counter += 1
    await interaction.response.edit_message(content = f"You clicked me {click_counter} times! :O")