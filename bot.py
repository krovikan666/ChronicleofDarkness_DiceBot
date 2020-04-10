import discord

from auth import token
from help import HelpHandler

from roller.initiative import Initiative
from roller.roller import Roller

client = discord.Client()


@client.event
async def on_ready():
    """Display a message when this bot joins a channel, and is ready"""

    message = discord.Game('$help for more info')
    await client.change_presence(activity=discord.Game(message))
    print('The bot is ready!')


@client.event
async def on_message(command):
    """Handles incoming messages and determines the following:

    1. Is this message for this bot?
    2. Which handler is responsible for this command?
    2a. Send command to the handler
    3. Ignore the message if we don't recognize it

    """

    if command.author == client.user or not command.content.startswith('$'):
        return
    elif command.content.startswith('$help'):
        await HelpHandler().handler(command)
    elif command.content.startswith('$roll'):
        await Roller(command.guild).handler(command)
    elif command.content.startswith('$init'):
        await Initiative(command.guild).handler(command)

client.run(token)
