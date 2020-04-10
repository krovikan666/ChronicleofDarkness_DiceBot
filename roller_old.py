import discord
import random
from error import EmbedError


class Roller():
    """The main dice roller for the dice bot

    :param int guild: The discord server the command was submitted on
    :type guild: :class: Discord.Guild

    :var dict emojis: The dictionary map of emojis that represent dice we are rolling

    """

    emojis = {
        1: ':one:',
        2: ':two:',
        3: ':three:',
        4: ':four:',
        5: ':five:',
        6: ':six:',
        7: ':seven:',
        8: ':eight:',
        9: ':nine:',
        10: ':zero:'
    }

    def __init__(self, guild):
        self.system_random = random.SystemRandom()

        for emoji in guild.emojis:
            if emoji.name.startswith('d10'):
                id = int(emoji.name[3:])
                self.emojis[id] = str(emoji)

    async def handler(self, command):
        """Handles incoming dice rolling commands

        :param command: The incoming command
        :type command: :class:`discord.Message`

        """

        split_message = command.content.split(' ')
        if len(split_message) < 2:
            await EmbedError().send_error(command.channel,
                                          'Incorrect command usage',
                                          'Error',
                                          'No command parameters',
                                          Roller.get_usage())
            return
        elif split_message[1] == 'chance':
            await self.roll_chance(command.channel, command.author)
        elif split_message[1].isdigit():
            rote = False
            roll_again = 10

            # get dice
            dice = int(split_message[1])

            # get roll again or rote flag
            try:
                roll_again = int(split_message[2])
            except IndexError:
                pass
            except ValueError:
                if split_message[2] == 'rote':
                    rote = True

            # get rote flag
            try:
                if split_message[3] == 'rote':
                    rote = True
            except IndexError:
                pass

            await self.roll_dice(command.channel, command.author, dice, roll_again, rote)
        else:
            await EmbedError().send_error(command.channel,
                                          'Incorrect command usage',
                                          'Error',
                                          'This is not a valid command {}'.format(command.content),
                                          Roller.get_usage())
            return

    async def roll_chance(self, channel, user):
        """Rolls a chance die for the user and sends it to the channel

        :param channel: The channel the command was sent to
        :type channel: :class: discord.GroupChannel
        :param user: The author of the command
        :type user: :class: discord.Member

        """

        colour = 0xFF00FF
        title = '{} chance'.format(user.display_name)

        die = self.get_die()
        extra_dice = self.explode_dice([die])

        embed = self.build_embed([die], extra_dice, 10)
        embed.title= title
        embed.colour = colour

        if die == 1:
            embed.set_footer(text='Dramatic Failure')

        await channel.send(embed=embed)

    async def roll_dice(self, channel, user, roll, explode=10, rote=False):
        """Rolls the dice for the user and sends the results to the channel

        :param channel: The channel the command was sent to
        :type channel: :class: discord.GroupChannel
        :param user: The author of the command
        :type user: :class: discord.Member
        :param int roll: The number of dice to roll
        :param int explode: the minimum number that causes a dice to explode, default: 10
        :param bool rote: If the action is a routine action

        """

        colour = 0x00FF33
        title = '{} rolled'.format(user.display_name)
        dice = []

        if roll > 30:
            await EmbedError().send_error(channel,
                                          'Too many dice',
                                          '$roll # #',
                                          'This bot only supports up to 30 dice')
            return
        elif explode < 6:
            await EmbedError().send_error(channel,
                                          'Incorrect roll again value',
                                          '$roll # #',
                                          'Incorrect roll again value, this bot only supports 6 through 10')
            return

        # Roll requested dice
        for c in range(0, roll, 1):
            die = self.get_die()
            if die < 8 and rote:
                die = self.get_die()
            dice.append(die)

        extra_dice = self.explode_dice(dice, explode)

        embed = self.build_embed(dice, extra_dice, 8)
        embed.title= title
        embed.colour = colour

        await channel.send(embed=embed)

    def build_embed(self, dice, extra_dice, success_value=8):
        """Builds and returns the embed for the dice result

        :param List dice: The list of dice that were rolled
        :param List extra_dice: The list of extra dice that were rolled
        :param int success_value: The min value for a success

        """

        message = ''
        extra_message = ''
        success = 0

        for die in dice:
            if die >= success_value:
                success += 1
            message += '{} '.format(self.emojis[die])

        for die in extra_dice:
            if die >= success_value:
                success += 1
            extra_message += '{} '.format(self.emojis[die])

        embed = discord.Embed()
        embed.add_field(name='Dice', value=message)
        embed.add_field(name='Successes', value=success)
        if extra_message:
            embed.add_field(name='Exploding Dice', value=extra_message, inline=False)

        return embed

    def explode_dice(self, dice, roll_again = 10):
        """Roll extra dice, and any further extras

        :param List dice: The list of dice that we are exploding
        :param roll_again: When we roll another die

        """

        extras = []

        for die in dice:
            if die < roll_again:
                continue
            while True:
                extra_die = self.get_die()
                extras.append(extra_die)
                if extra_die < roll_again:
                    break

        return extras

    def get_die(self):
        """Returns a random number between 1 and 10"""

        return self.system_random.randint(1, 10)

    @staticmethod
    def get_usage():
        """Returns the usage embed of the command"""

        usage = discord.Embed(title='roll command')
        usage.add_field(name='usage', value='$roll chance / $roll # # (rote)', inline=False)
        usage.add_field(name='$roll chance', value='will roll a chance die for you ', inline=False)
        usage.add_field(name='$roll X', value='will roll X dice for you, with 10-again rules', inline=False)
        usage.add_field(name='$roll X rote',
                        value='will roll X dice for you, with 10-again rules, rote rules',
                        inline=False)
        usage.add_field(name='$roll X Y', value='will roll X dice for you, with Y-again rules', inline=False)
        usage.add_field(name='$roll X Y rote',
                        value='will roll X dice for you, with Y-again rules, rote rules',
                        inline=False)

        return usage
