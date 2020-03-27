from discord import Embed


class EmbedError():
    """Creates and sends an error message to the channel

    :var int colour: The colour we will use for the error messages

    """

    colour = 0xFF2400

    async def send_error(self, channel, title, name, value, embed=None):
        """Send an error message to the channel"""

        if not embed:
            embed = Embed()
        embed.title = title
        embed.color = self.colour
        embed.insert_field_at(index=0, name=name, value=value, inline=False)
        await channel.send(embed=embed)
