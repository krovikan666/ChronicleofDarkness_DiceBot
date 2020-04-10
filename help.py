from discord import Embed
from error import EmbedError
from roller.roller import Roller


class HelpHandler():
    """Handles help requests for the bot

    :var int colour: The colour we will use for the help messages

    """

    colour = 0x00BFFF

    async def handler(self, command):
        """Send an error message to the channel

        :param command: The incoming command
        :type command: :class:`discord.Message`

        """

        if command.content == '$help':
            await self.default_help(command.channel)
        elif 'roll' in command.content:
            await self.roll_help(command.channel)
        else:
            await EmbedError().send_error(command.channel,
                                          'Invalid help command',
                                          '$help <command>',
                                          'Type $help for more information')

    async def default_help(self, channel):
        """Sends the default help message to the channel

        :param channel: The channel the command was sent to
        :type channel: :class: discord.GroupChannel

        """

        embed = Embed(color=self.colour)
        embed.add_field(name='$help', value='This is the information I am showing you now', inline=False)
        embed.add_field(name='$help <command>', value='I will show you information about a specific command',
                        inline=False)
        embed.add_field(name='$roll', value='I will roll some dice for you', inline=False)
        await channel.send(embed=embed)

    async def roll_help(self, channel):
        """Sends the roll help message to the channel

        :param channel: The channel the command was sent to
        :type channel: :class: discord.GroupChannel

        """

        embed = Roller.get_usage()
        embed.color = self.colour
        await channel.send(embed=embed)
