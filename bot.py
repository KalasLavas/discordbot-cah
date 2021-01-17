# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

client = discord.Client(intents=intents)

murad_id = 605470759682572288;

@client.event
async def on_ready():
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


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "/whoami":
        if message.author.id == murad_id:
            response = "You are a stupid dumbass"
        else:
            response = f"You are {message.author.name}"
        await message.reply(response)


client.run(TOKEN)