import random
from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    """The base dice rolling class

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

    @abstractmethod
    async def handler(self, command):
        """Abstract definition for handler"""
        pass

    @abstractmethod
    def build_embed(self):
        """Abstract definition of building an embed"""
        pass

    def get_die(self):
        """Returns a random number between 1 and 10"""

        return self.system_random.randint(1, 10)

    @staticmethod
    @abstractmethod
    def get_usage():
        """Abstract definition of getting the command usage"""
        pass
