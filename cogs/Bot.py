import discord
from discord.ext import commands
from discord import app_commands

class Bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        '''when bot is online, set status and print to console'''
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f'The Game of Life'))
        print('------')
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id}!)')
        print('------')
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        '''listens for "Hello there."'''
        if message.content == "Hello there.":
            await message.channel.send("General Kenobi.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member) -> None:
        '''when anyone reacts with 😳, send 😳 to channel'''
        if reaction.emoji == "😳":
            await reaction.message.channel.send('😳')

async def setup(bot: commands.Bot):
    await bot.add_cog(Bot(bot))