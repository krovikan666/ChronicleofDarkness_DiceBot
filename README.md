# Chronicle of Darkness - Dice Bot 

This is a simple d10 dice roller for the Chronicles of Darkness by White Wolf

## Note

This is a small dice bot that I created so we could continue playing RPGs online during 
the COVID-19 outbreak.
Under the emjis directory I have included the custom emojis I created for our server feel
free to use them (or use your own).
By default, this bot will just use the discord number emojis.

## Setup

1. Log into https://discordapp.com/developers/applications/
1. Create a new application
1. Navigate to the Bot section
1. Populate the token in auth.py
1. Navigate to the OAuth2 section
1. Select bot
1. Select the permissions for the bot
1. Copy the link and use it to join the bot to your server
1. Start the python bot by importing client from bot.py

## Required Permissions

- Send messages
- Manage messages
- Use external emjois
- Manage emojis
- View channels

## Custom Emojis

If you have emojis with d10# as the alias on the discord server, this bot will pick them up
and use them in place of the default emojiis.
