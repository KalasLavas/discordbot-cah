'''Main bot file'''
import os
import sys
import discord
from dotenv import load_dotenv

class MyClient(discord.Client):
    '''discord class redefinition'''
    async def on_ready(self):
        '''executed when connected to discord'''
        print(f"{client.user} has connected to Discord!")

        if len(client.guilds) == 0:
            print("Alone and drunk.")
            sys.exit()

        if len(client.guilds) > 1:
            print("Where e-girls")
            sys.exit()

        guild = client.guilds[0]

        owner = guild.owner

        print(f"{guild.name}: {guild.id}; owner: {owner}")

        print("Members:")
        for member in guild.members:
            print(f"    {member.name}: {member.id}")

        print("Channels:")
        for channel in guild.channels:
            print(f"    {channel.name}: {channel.type}")

    async def on_message(self, message):
        '''executed when new message is received'''
        if message.author == client.user:
            return

        if message.content.startswith('/'): #Add custom prefix
            args = message.content[len('/'):].split()
            print(args)
            await (await bf.function(args[0]))(self, message, args[1:])

import bot_functions as bf

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    client = MyClient(intents=discord.Intents.all())
    print("Connecting to Discord ...")
    client.run(TOKEN)
