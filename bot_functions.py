import requests
import discord
import bot
import cah

game = cah.CAH()

async def latex(bot, message, args):
    tex = ' '.join(args);
    
    url = "http://latex2png.com/api/convert"
    data = {
        "auth":{
            "user":"guest",
            "password":"guest"
        },
        "latex": tex,
        "resolution": 250,
        "colour":"ffffff"
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

async def chandle_err(bot, status, message):
    embed = discord.Embed(title="Fucking ermeni", description="BLYAT :pogmurad:", colour=0xff0000)   
    if status == -1:
        embed = discord.Embed(title=f"{message.author.name} boyun çatmayan yerə, burnuvu soxma", description="BLYAT <:pogmurad:797922214447677491>", colour=0xff0000)
    if status == -2:
        embed = discord.Embed(title=f"{message.author.name} sən saymağı öyrənməlisən", description="BLYAT <:pogmurad:797922214447677491>", colour=0xff0000)
    if status == -3:
        embed = discord.Embed(title=f"{message.author.name} TƏLƏSMƏ", description="BLYAT <:pogmurad:797922214447677491>", colour=0xff0000)
    if status == -4:
        embed = discord.Embed(title=f"{message.author.name} LOM, yazdığından xəbərin var?!", description="BLYAT <:pogmurad:797922214447677491>", colour=0xff0000)
    if status == -5:
        embed = discord.Embed(title=f"{message.author.name} sən kralsan a.k.a. göt", description="BLYAT <:pogmurad:797922214447677491>", colour=0xff0000)
    if status == -6:
        embed = discord.Embed(title=f"{message.author.name} sən kral olmasanda, yenədə götsən", description="BLYAT <:pogmurad:797922214447677491>", colour=0xff0000)
    await message.reply(embed=embed)
    return 0

async def cjoin(bot, message, args):

    await game.join(message.author.id)
    embed = discord.Embed(title=f"{message.author.name} oyuna qoşuldu", description=("Oyunu başlatmaq üçün /start daxil edin" if message.author.id == game.master else f"Oyunu başlatmaq üçün {bot.get_user(game.master).name}-ı gözlə"))
    await message.reply(embed=embed)

async def clist(bot, message, args):
    players = await game.list()
    lb = []
    for player in players:
        user = bot.get_user(player).name
        lb.append((players[player][0], user));

    lb.sort(reverse=True)
    lbstr = ""
    for player in lb:
        lbstr += f"{player[1]}: **{player[0]}**\n" 
    embed = discord.Embed(title="Leaderboard 🏆", description=lbstr, colour=0xffff00)
    if game.mainserver is None:
        game.mainserver = message.channel
    await game.mainserver.send(embed=embed) 
    

async def cstart(bot, message, args):
    status = await game.start(message.author.id)

    if status<0:
        return await chandle_err(bot, status, message) 
    
    game.mainserver = message.channel

    await cinitgame(bot, message, args)

# /pick
async def cpick(bot, message, args):
    print([i.strip() for i in ' '.join(args).split(',')])
    status = await game.playervote(message.author.id, [int(i.strip()) for i in ' '.join(args).split(',')])
    if status<0:
        return await chandle_err(bot, status, message)
    embed= discord.Embed(title=f"{message.author.name} seçimini tamamladı", description=(f"{len(game.players)-len(game.voted)-1} nəfər qalıb" if status != 0 else "Kralın növbəsidir"), color=0x00ff00)
    await message.reply(embed=embed)
    await game.mainserver.send(embed=embed)

    if 0<status:
        return
    votes = await game.initiateczarvote();
    
    s = ""
    print(votes)
    for i,vote in enumerate(votes):
        print(i)
        print(votes[i])
        print(votes[i][1])
        s+= f"{i+1}: {votes[i][1]}\n"
        for j in range(2,len(votes[i])):
            s+= f"    {votes[i][j]}\n"
        s+='\n'
    embed = discord.Embed(title=f"{bot.get_user(game.czar).name}, nömrə 1 loxu seç.", description="Ədədi yazaraq seç", colour=0x0000ff)
    await game.mainserver.send(embed=embed)
    
    embed = discord.Embed(title=f"{game.black[0][0]}", description=s, colour=0x00ff00)
    await game.mainserver.send(embed=embed)

    def check_for_czar(m):
        print(m.author.id)
        print(game.czar)
        print(m.content)
        print(len(game.players))
        print('')
        try:
            if m.author.id == game.czar and 0<int(m.content) and int(m.content)<len(game.players):
                return True
            return False
        except:
            return False
    
    newmsg = await bot.wait_for('message', check=check_for_czar)

    winner = await game.czarvote(newmsg.author.id, int(newmsg.content))

    s=""
    for j in winner[2]:
            s+= f"{j}\n"

    embed = discord.Embed(title=f"Təbriklər, {bot.get_user(winner[0]).name}", description="", colour=0xffff00)
    embed.add_field(name=f"{winner[1][0]}",value=f"{s}",inline=False)
    await game.mainserver.send(embed=embed)
    await clist(bot, message, args)

    await cinitgame(bot, message, args)
    

async def cinitgame(bot, message, args):
    black = await game.initiateplayervote()
    Bembed = discord.Embed(title=f"{black[0]}", description=f"{black[1]} kart seçmək lazımdır\n/pick 1,6,3\n**Kral {bot.get_user(game.czar).name}-dır**", color=0x000000)
    await game.mainserver.send(embed=Bembed) 
    
    players = await game.list()
    for player in players:
        if player == game.czar:
            continue
        mycards = ""
        for i,line in enumerate(players[player][1]):
            mycards = f"{mycards}{i+1}: {line} \n" 
        Wembed = discord.Embed(title=f"{bot.get_user(player).name}, sənin kartların", description=mycards, color=0xffffff)
        channel = bot.get_user(player).dm_channel
        if channel is None:
            channel = await bot.get_user(player).create_dm()
        await channel.send(embed=Bembed) 
        await channel.send(embed=Wembed) 

async def cend(bot, message, args):
    global game
    if await game.end(message.author.id) != 0:
        return await chandle_err(bot, -1, message)
    await clist(bot, message, args)
    game = cah.CAH()

async def invalid_func(*args, **kwargs):
    return

func_list={
    "latex": latex,
    "list": clist,
    "join": cjoin,
    "start": cstart,
    "pick": cpick,
    "end": cend,
}

async def function(key):
    if func_list.get(str(key)) is None:
        return invalid_func

    return func_list[key]
