import requests
import discord

async def latex(message, args):
	print(args)
	tex = ' '.join(args);
	
	url = "http://latex2png.com/api/convert"
	json = '{"auth":{"user":"guest","password":"guest"},"latex":"cos^2 xy","resolution":100,"color":"ffffff"}'
	
	r = requests.post(url = url, data = json)
	if r.status_code != 200:
		return
	
	data = r.json()
	
	if data["result-code"]:
		return

	await message.reply(file=discord.File("http://latex2png.com"+data["url"]));


async def invalid_func(*args, **kwargs):
	return

func_list={
	"latex": latex
}

async def function(key):
	if func_list.get(str(key)) == None:
		return invalid_func
	return func_list[key]

import bot