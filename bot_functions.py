import requests
import discord

async def latex(message, args):
	tex = ' '.join(args);
	
	url = "http://latex2png.com/api/convert"
	data = {
		"auth":{
			"user":"guest",
			"password":"guest"
		},
		"latex": tex,
		"resolution": 250,
		"color":"ffffff"
	}
	json = str(data).replace("'",'"')
	r = requests.post(url = url, data = json)
	
	if r.status_code != 200:
		print(r.status_code)
		return
	
	data = r.json()
	
	if data["result-code"]:
		print(f'data: {data}')
		return

	await message.reply("http://latex2png.com"+data["url"]);


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