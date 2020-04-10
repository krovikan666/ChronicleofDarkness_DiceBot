import discord
from error import EmbedError
from roller.base import Base


class Initiative(Base):
    """The initiative roller for the dice bot

    :param int guild: The discord server the command was submitted on
    :type guild: :class: Discord.Guild

    :var dict emojis: The dictionary map of emojis that represent dice we are rolling

    """

    result_emojis = {
        1: ':one:',
        2: ':two:',
        3: ':three:',
        4: ':four:',
        5: ':five:',
        6: ':six:',
        7: ':seven:',
        8: ':eight:',
        9: ':nine:',
        0: ':zero:'
    }

    def __init__(self, guild):
        super().__init__(guild)

    async def handler(self, command):
        """Handles incoming initiative commands

        :param command: The incoming command
        :type command: :class:`discord.Message`

        """

        split_message = command.content.split(' ')
        if len(split_message) < 2 or not split_message[1].isdigit():
            await EmbedError().send_error(command.channel,
                                          'Incorrect command usage',
                                          'Error',
                                          'No command parameters',
                                          Initiative.get_usage())
            return

        # get modifier
        modifier = int(split_message[1])

        await self.roll_initiative(command.channel, command.author, modifier)

    async def roll_initiative(self, channel, user, modifier):
        """Rolls a chance die for the user and sends it to the channel

        :param channel: The channel the command was sent to
        :type channel: :class: discord.GroupChannel
        :param user: The author of the command
        :type user: :class: discord.Member
        :param int modifier: How much to add to the dice roll

        """

        colour = 0xFF6500
        title = '{} initiative'.format(user.display_name)

        die = self.get_die()
        initiative = die + modifier

        embed = self.build_embed(die, initiative)
        embed.title= title
        embed.colour = colour

        await channel.send(embed=embed)

    def build_embed(self, die, initiative):
        """Builds and returns the embed for the dice result

        :param int die: The die that we rolled
        :param int initiative: The total initiative

        """

        roll_message = ''
        result_message = ''

        roll_message += '{} '.format(self.emojis[die])


        for digit in list(str(initiative)):
            result_message += '{} '.format(self.result_emojis[int(digit)])

        embed = discord.Embed()
        embed.add_field(name='Roll', value=roll_message)
        embed.add_field(name='Initiative', value=result_message)

        return embed

    @staticmethod
    def get_usage():
        """Returns the usage embed of the command"""

        usage = discord.Embed(title='Initiative command')
        usage.add_field(name='usage', value='$init #', inline=False)
        usage.add_field(name='$init modifier', value='will roll your initiative and add your modifier ', inline=False)

        return usage
