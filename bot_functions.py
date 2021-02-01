import requests
import discord
import bot

async def invalid_func(*args, **kwargs):
    '''function not found'''
    return

func_list = {
    
}

async def function(key):
    '''Call function by its codename'''
    if func_list.get(str(key)) is None:
        return invalid_func

    return func_list[key]
