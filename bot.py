import logging
import logging.handlers
import os
import time
from typing import Literal

import aiosqlite
import discord
from discord import app_commands
from dotenv import load_dotenv

from census_client import main


# Check if bot.py is in a container
def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )
docker = is_docker()
# Change secrets variables accordingly
if docker == True: # Use Docker ENV variables
    TOKEN = os.environ['DISCORD_TOKEN']
    LOG_LEVEL = os.environ['LOG_LEVEL']

else: # Use .env file for secrets
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    LOG_LEVEL = os.getenv('LOG_LEVEL')

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# Configure logging
class CustomFormatter(logging.Formatter): # Formatter

    grey = "\x1b[38;20m"
    blue = "\x1b[34m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        dt_fmt = '%m/%d/%Y %I:%M:%S'
        formatter = logging.Formatter(log_fmt, dt_fmt)
        return formatter.format(record)

# Create logger
logging.getLogger('discord.http').setLevel(logging.INFO)
log = logging.getLogger('discord')
if LOG_LEVEL is None:
    log.setLevel(logging.INFO)
else:
    log.setLevel(LOG_LEVEL)

handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
log.addHandler(handler)
# Disable VoiceClient warnings
discord.VoiceClient.warn_nacl = False

# Check for continents.db
db_exists = os.path.exists('continents.db')
if db_exists == False:
    log.error("Database does not exist!")

# Setup Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Collect data from db and create embed
async def get_from_db(server: str):
    db = await aiosqlite.connect('continents.db')
    sql = f"""
    SELECT * FROM {server}
    """
    async with db.execute(sql) as cursor: # Execute query
        embedVar = discord.Embed(title=server[0].upper() + server[1:], color=0x5865F2, timestamp=discord.utils.utcnow()) # Create embed title
        row_timestamps = []
        async for row in cursor:
            cont = row[1] # Row 1 is continents
            cont = cont[0].upper() + cont[1:] # Captialize
            status_emoji = {
                'open': '🟢 Open  ',
                'closed': '🔴 Closed'
            }
            status = status_emoji[row[2]] # Format status
            embedVar.add_field(name=cont, value=status, inline=True) # Create embed fields
            row_timestamps.append(row[3]) # Record timestamps
        embedVar.add_field(name="\u200B", value="\u200B", inline=True) # Blank field to fill 3x3 space
        data_age = round(time.time() - max(row_timestamps))
        embedVar.set_footer(text=f"Data from {data_age}s ago", icon_url="https://raw.githubusercontent.com/wupasscat/wupasscat/main/profile.png")
        if data_age > 300:
            log.warning("Data is older than 5 minutes! Retrying")
            await main()
    await db.close()
    return embedVar

# Discord
# Refresh button
class MyView(discord.ui.View):
    def __init__(self, server):
        super().__init__(timeout=None)
        self.server = server
    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.primary, emoji="🔄")
    async def refresh_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        log.info(f"Refresh /continents triggered for {self.server[0].upper() + self.server[1:]}")
        embedVar = await get_from_db(self.server)
        await interaction.response.edit_message(embed=embedVar, view=self)

# /continents
@tree.command(name = "continents", description = "See open continents on a server")
async def continents(interaction, server: Literal['Connery', 'Miller', 'Cobalt', 'Emerald', 'Jaeger', 'Soltech']):
    log.info(f"Command /continents triggered for {server}")
    server = server[0].lower() + server[1:]
    embedVar = await get_from_db(server)
    await interaction.response.send_message(embed=embedVar, view=MyView(server))

@client.event
async def on_ready():
    await tree.sync()
    log.info('Bot has logged in as {0.user}'.format(client))
    await main() # Run census_client.py

client.run(TOKEN, log_handler=None)