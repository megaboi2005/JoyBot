#imports
import os
import random
import discord
from discord.ext import commands
import json
import asyncio
import time
import emoji


##global variables
client = discord.Client()
client = commands.Bot(command_prefix = '.')
topuser = 'no one'
@client.event
async def on_message(message):
    def xp(operation, amount, message):
        global complete
        try:
            user = open('database/' + str(message.author.id) + '.json', "r")

            info = json.loads(user.read())
            #topfile = open('name','r')
            #topuser = json.loads(topfile.read())
            #if not str(message.author.id) == topuser["name"]:
            #    info2 = json.load(topfile.read())
            #    if int(info2["xp"]) >= int(info["xp"]):
            #        topfile = open('name', 'w')
            #        topfile.write('{"xp"="'+info["xp"]+'"}')


            user.close()
            user = open('database/' + str(message.author.id) + '.json', "w")
            xpstart = info["xp"]
            inventory = info["inv"]
            invamount = info["invamount"]
            if operation == 'add':
                xp = int(xpstart) + amount
            if operation == 'subtract':
                xp = int(xpstart) - amount
            if xp < 0:
                complete = False
                user.write('{ "xp":"' + str(xpstart) + '","inv":"' + inventory + '","invamount":"' + invamount + '"}')
                user.close()
                return



            complete = True
            if xp > 0:
                user.write('{ "xp":"' + str(xp) + '","inv":"' + inventory + '","invamount":"' + invamount + '"}')
        except FileNotFoundError:

            user = open('database/' + str(message.author.id) + '.json', "x")
            user.write('{ "xp":"0","inv":"0","invamount":"0"}')
        user.close()
    if message.author == client.user:
        return

    string = message.content.split(' ')
    cmd = string[0].lower()
    try:
        output = message.content.split(' ', 1)[1]
    except IndexError:
        output = ''
    try:
        args = string[1].lower()

    except IndexError:
        args = ''
    try:

        print('(', message.guild.name, ')',message.author, ':', message.content)
        try:
            log = open('log.txt','a')
            log.write(f'({message.guild.name}){message.author}:{message.content}\n')
        except UnicodeEncodeError:
            log = open('log.txt','a')
            log.write(f'({message.guild.name}){message.author}:{emoji.demojize(message.content)}\n')
    except AttributeError:
        print('(',message.author, ':', message.content)

    xp('add',1,message)






##commands
    ##help
    if cmd == '$help':

        file = open('help.txt', "r")
        helpmenu = file.read().split('^')
        try:
            try:
                embedVar = discord.Embed(title="JoyHelp", description="If you have any questions ask megaboi#2627",color=0x00ff00)
                embedVar.add_field(name="Help", value=helpmenu[int(args)], inline=False)
            except ValueError:
                embedVar = discord.Embed(title="JoyHelp", description="If you have any questions ask megaboi#2627",color=0x00ff00)
                embedVar.add_field(name="Help", value=helpmenu[0], inline=False)
        except IndexError:
            await message.channel.send('help page could not be found - ERROR 404')
        await message.channel.send(embed=embedVar)


    ##info
    if cmd == '$info' or cmd == '$stats':
        if args == '':
            user = open('database/' + str(message.author.id) + '.json', "r")
            info = json.loads(user.read())
            await message.channel.send('stats for '+ str(message.author.mention))
            await message.channel.send('xp: '+info["xp"])
        else:
            try:
                if args.startswith('<@'):
                    user = open('database/' + str(args)[3:-1] + '.json', "r")
                    await message.channel.send('stats for ' + args)
                else:
                    user = open('database/' + str(args) + '.json', "r")
                    await message.channel.send('stats for <@!' + args + '>')
                info = json.loads(user.read())

                await message.channel.send('xp: ' + info["xp"])
            except OSError:
                await message.channel.send('Failed to find that user in our database - ERROR 404')
                return

    ##STORE

    ##buy command
    if cmd == '$buy':
        if args == 'list':
            list = os.listdir('shop')
            embedVar = discord.Embed(title="JoyShop", description="If you have any questions or suggestions ask megaboi#2627",color=0x00ff00)

            for x in list:

                item = open('shop/'+x)
                itemparse = json.loads(item.read())
                embedVar.add_field(name=itemparse["name"], value=itemparse["price"], inline=False)
                #await message.channel.send(itemparse["name"] + ' - '+ itemparse["price"])
            await message.channel.send(embed=embedVar)
        else:
            try:
                item = open('shop/'+args,"r")
                itemparse = json.loads(item.read())
                xp('subtract', int(itemparse["price"]), message)
                if complete == False:
                    await message.channel.send('you cannot afford this item')

            except json.decoder.JSONDecodeError:
                await message.channel.send('this item does not exist')
                return






    ##randomperson
    if cmd == '$randomperson' or cmd == '$ranper':
        status = await message.channel.send('Downloading...')
        os.system('curl -o person.png https://thispersondoesnotexist.com/image')
        await status.edit(content="Uploading....")
        await message.channel.send(file = discord.File('person.png'))
        await status.delete()
        os.remove("person.png")

    ##randomcrab
    if cmd == '$randomcrab' or cmd == '$rancrab':
        files = os.listdir('crabs')
        outcome = random.choice(files)
        status = await message.channel.send('Uploading...')
        await message.channel.send(file=discord.File('crabs/'+outcome))
        await status.delete()
    ##ECHO
    if cmd == '$echo':
        await message.channel.send(output)

    ##attract
    #if cmd == '$attract':
        #await message.channel.send('hi! I realize this might come off as a bit odd haha.. but before the whole quarantine thing I saw you around school, and you seem really cool. If you arent interested in talking thats alright, no worries!')
##roll dice
    if cmd == '$roll':
        numbers = ["1", "2", "3", "4", "5", "6"]
        picked = random.choice(numbers)
        output = await message.channel.send('rolling....')
        time.sleep(2)
        await output.edit(content='you rolled and got a ' + picked)

    ##ping
    if cmd == '$ping':
        await message.channel.send('pong!')

        await message.channel.send(client.latency)

    ##8ball
    if cmd == '$8ball':
        outcomes = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Outlook good.", "Reply hazy, try again.","Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.", "Yes – definitely.", "You may rely on it."]

        picked2 = random.choice(outcomes)
        await message.channel.send(picked2)

    ##quote
    if cmd == '$randomquote' or cmd == '$ranquote':
        status = await message.channel.send('Downloading text file...')
        os.system('curl https://inspirobot.me/api?generate=true --output url.txt')
        url = open('url.txt', 'r').read().replace('\n', ' ')
        #print(url)
        await status.edit(content ='Downloading image...')
        os.system(f'curl {url} --output quote.png')
        await status.edit(content="Uploading....")
        await message.channel.send(file=discord.File('quote.png'))
        await status.delete()
    ##joke
    if cmd == '$randomjoke' or cmd == '$joke':
        status = await message.channel.send('Downloading the funny...')
        os.system('curl -k "https://v2.jokeapi.dev/joke/Any?blacklistFlags=religious,racist,sexist&format=txt" --output joke.txt')
        joke = open('joke.txt', 'r')
        await status.edit(content=joke.read())



    ##test



async def ch_pr():
    await client.wait_until_ready()
    added = 0
    statuses = ["BALLS","Minecraft","Dead By Daylight","$help lol"]

    while not client.is_closed():

        try:
            status = statuses[added]
        except IndexError:
            added = 0
        await client.change_presence(activity=discord.Game(name=status,))
        added += 1
        await asyncio.sleep(10)
client.loop.create_task(ch_pr())

client.run('token')
