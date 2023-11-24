import discord
from discord import app_commands
from discord.ext import commands, tasks
from PIL import Image, ImageDraw
import string
import random
from util.funcs import generate_verification_code, InteractionCheck
from config import Config
# Setup logging config
class aclient(discord.Client):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
        print('Logged in')

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = 'verify', description = "Verify your access to the discord using Captcha")
async def self(interaction: discord.Interaction):
    if len(interaction.user.roles) > 1:
        await interaction.response.send_message(content="You have already been verified!",ephemeral=True)
    else:
        await generate_verification_code(interaction)
    

client.run(Config.t)