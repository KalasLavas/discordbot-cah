# import requests
import discord
#import bot
import csgostash

async def csgo_stash_search(bot, message, args):
    l = await search(query=' '.join(args), count=3)
    for item in l:
        embed = discord.Embed(title=item["name"], url=item["link"], description=f"**{item['price']}**", color=item["color"])
        embed.set_thumbnail(url=item["thumbnail"])
        await message.channel.send(embed=embed)


async def invalid_func(*args, **kwargs):
    '''function not found'''
    return

func_list = {
    "market": csgo_stash_search,
}

async def function(key):
    '''Call function by its codename'''
    if func_list.get(str(key)) is None:
        return invalid_func

    return func_list[key]
