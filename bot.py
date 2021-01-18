# bot.py
import os

import discord
from dotenv import load_dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"{client.user} has connected to Discord!")
        
        if(len(client.guilds) == 0):
            print("Alone and drunk.")
            exit()
        
        if(len(client.guilds) > 1):
            print("Where e-girls")
            exit()

        guild = client.guilds[0];

        owner = guild.owner

        print(f"{guild.name}: {guild.id}")

        print("Members:")
        for member in guild.members:
            print(f"    {member.name}: {member.id}")

        print("Channels:")
        for channel in guild.channels:
            print(f"    {channel.name}: {channel.type}")

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('/'): #Add custom prefix
            args = message.content[len('/'):].split()
            print(args)
            await message.channel. trigger_typing()
            await (await bf.function(args[0]))(message,args[1:]) 

        # if 
        #     if message.author.id == murad_id:
        #         response = "You are a stupid dumbass"
        #     else:
        #         response = f"You are {message.author.name}"
        #     await message.reply(response)

import bot_functions as bf

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    client = MyClient(intents=discord.Intents.all())
    print("Connecting to Discord ...")
    client.run(TOKEN)