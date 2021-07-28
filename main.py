#imports
import os
import random
import discord
from discord.ext import commands
import json


##global variables
client = discord.Client()
client = commands.Bot(command_prefix = '.')

@client.event
async def on_message(message):
    def xp(operation, amount, message):
        global complete
        try:
            user = open('database/' + str(message.author.id) + '.json', "r")
            info = json.loads(user.read())
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
        os.system('curl -o person.png https://thispersondoesnotexist.com/image')
        await message.channel.send(file=discord.File('person.png'))
        os.remove("person.png")

    ##randomcrab
    if cmd == '$randomcrab' or cmd == '$rancrab':
        files = os.listdir('crabs')
        outcome = random.choice(files)
        await message.channel.send(file=discord.File('crabs/'+outcome))

    ##ECHO
    if cmd == '$echo':
        await message.channel.send(output)

    ##add
    #if cmd == '$add':
        #final = 0
        #outcome = output.split()
        #for x in outcome:

            #print(outcome[x])
            #final += int(add)

        #await message.channel.send(final)

    ##test


client.run('token')