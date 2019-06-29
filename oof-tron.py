import discord  # Discord API
from discord.ext import commands  

token = open("token.txt", "r")  # File the token is in
token = token.read()
prefix = open("prefix.txt", "r")  # File the prefix is in, default is nothing ("")
prefix = prefix.read()
client = commands.Bot(command_prefix=prefix)

client.remove_command('help')  # Removed the default help command cause it's not really helpful

vol = 5  # Default Volume the bot has
pitch = 1  # Default pitch the bot has


@client.event
async def on_ready():  # Once the bot starts the code block below will run
    print("Oof")

    
# @client.command()  # For testing
# async def test(ctx):
#
#    await ctx.send("ok")
  
    
@client.command(pass_context=True, aliases=['oof.h', 'oof.help'])
async def oof_help(ctx):
    embed = discord.Embed(title="~Oof Bot's Commands~", color=0xffff80)
    embed.add_field(name="oof.help", value="duh", inline=False)
    embed.add_field(name="oof", value="Oofs you real hard", inline=False)
    embed.add_field(name="bruh", value="Bruh", inline=False)
    embed.add_field(name="za warudo", value="brpfbbbbbbbbbb", inline=False)
    embed.add_field(name="alexa Play Despacito", value="Despacito but less worse and much better", inline=False)
    embed.add_field(name="here come dat boi", value="oh shit waddup", inline=False)
    embed.add_field(name="volume", value="Less ear-death", inline=False)
    embed.add_field(name="prefix", value="Changes the prefix (must restart bot)", inline=False)
    embed.add_field(name="Some secret stuff", value="Check the code, im too lazy to write them down", inline=False)
    await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=['p', 'prefix'])
async def set_prefix(ctx, prefix_str: str = ""):
    if prefix_str == "":
        prefix_user = ""
    await ctx.send("Prefix set to %s, restart the bot for the change to take effect" % prefix_str)
    prefix_user = open("prefix.txt", "w")  # File the prefix is in, default is nothing ("")
    prefix_user.write(prefix_str)

    
# Volume Command, changes the volume of the sounds
@client.command(pass_context=True, aliases=['v', 'vol'])
async def volume(ctx, num_pre: str):

    global vol  # Is global so it can be accessed from other functions

    if num_pre == "":
        await ctx.send("Volume level is at %s" % vol)

    try:
        vol = float(num_pre)
    except ValueError:
        await ctx.send("Volume must be a number")
        vol = 5

    if vol > 100:
        await ctx.send("Value too big (must be between 0 and 100)")
    elif vol < 0:
        await ctx.send("Value too small (must be between 0 and 100)")
    else:
        await ctx.send("Volume is now set to %s" % vol)
        vol = vol / 10  # Because ffmpeg gets values from 1-10


# oof.oof command
@client.command(pass_context=True, aliases=['', "oof"])  # -oof or - or -normal
async def Oof(ctx, par: str = "1"):  # Default pitch value = 1

    global source, pitch, vc, sound_file
    sound_file = "oof.mp3"
    pitch = 1

    try:
        par = par.lower()
        pitch = float(par)
    except ValueError:
        if par == "high":
            pitch = 5
        elif par == "ultra_high":
            pitch = 9

        elif par == "heliumed":
            sound_file = "heliumed.mp3"
        elif par == "chewbacca":
            sound_file = "chewbacca.mp3"
        elif par == "demon":
            sound_file = "demon.mp3"
        elif par == "oofs":
            sound_file = "oofs.mp3"

    if pitch > 1:
        pitch = (pitch / 10) + 1  # Adds more functionality to the command
    elif pitch > 100:  # max(pitch)
        pitch = 100
    elif 0 < pitch < 0.10:
        pitch = 0.5  # min(pitch)
    elif pitch < 0:
        pitch = 0.5
    source = discord.FFmpegPCMAudio('resources\\%s' % sound_file, options="-filter:a 'volume=%s, asetrate=44100*%s'" % (vol, pitch))
    # ^ the source that is later played with some editing

    voice_state = ctx.message.author.voice  # Voice state of author

    if voice_state is None:  # None means user is not connected to channel
        await ctx.send("You have to be connected in a channel to use this command")

    else:

        try:
            global vc
            vc = await voice_state.channel.connect()  # Voice Connection
        except discord.ClientException:  # If the client is already connected to a channel
            pass

        try:
            vc.play(source)
            await ctx.send("Oof")
        except discord.ext.commands.errors.CommandInvokeError:
            vc.stop()

        try:
            @client.command(pass_context=True, aliases=['l', 'exit', 'e'])
            async def leave(ctx):
                await vc.disconnect()
        except discord.ClientException:
            pass


@client.command(pass_context=True)
async def bruh(ctx):

    source = discord.FFmpegPCMAudio('resources\\bruh.mp3', options="-filter:a 'volume=%s'" % vol)

    voice_state = ctx.message.author.voice  # Voice state of author
    if voice_state is None:  # None means user is not connected to channel
        await ctx.send("You have to be connected in a channel to use this command")
    else:
        try:
            global vc
            vc = await voice_state.channel.connect()  # Voice Connection
        except discord.ClientException:  # If the client is already connected to a channel
            pass

        try:
            vc.play(source)
            await ctx.send("Bruh")
        except discord.ext.commands.errors.CommandInvokeError:
            vc.stop()

        try:
            @client.command(pass_context=True, aliases=['l', 'exit', 'e'])
            async def leave(ctx):
                await vc.disconnect()
        except discord.ClientException:
            pass


@client.event
async def on_message(message):
    alexa = ['thisissosadalexaplaydespacito', 'alexaplaydespacito']
    world = ['zawarudo', 'theworld']
    remove = [",", " ", "_"]

    channel = message.channel
    msg = message.content
    i = 0

    msg = msg.lower()  # Make all the letters lower case
    msg = msg.replace(remove[0], "").replace(remove[1], "").replace(remove[2], "")

    if msg.startswith("herecomedatboi"):
        await channel.send("oh shit waddup")

    elif msg.startswith(alexa[0]) or msg.startswith(alexa[1]):  # I know this is bad coding
        # but the contest will be over soon and I still haven't finished lol
        voice_state = message.author.voice
        source = discord.FFmpegPCMAudio('resources\\despacito.mp3', options="-filter:a 'volume=%s'" % vol)

        if voice_state is None:  # None means user is not connected to channel
            await message.author.server.send("You have to be connected in a channel to use this command")
        else:
            try:
                global vc
                vc = await voice_state.channel.connect()  # Voice Connection
            except discord.ClientException:  # If the client is already connected to a channel
                pass
            try:
                vc.play(source)
            except discord.ext.commands.errors.CommandInvokeError:
                vc.stop()

    elif msg.startswith(world[0]) or msg.startswith(world[1]):  # I know this is bad coding
        # but the contest will be over soon and I still haven't finished lol
        voice_state = message.author.voice
        source = discord.FFmpegPCMAudio('resources\\za_warudo.mp3', options="-filter:a 'volume=%s'" % vol)

        if voice_state is None:  # None means user is not connected to channel
            await message.author.server.send("You have to be connected in a channel to use this command")
        else:
            try:
                vc = await voice_state.channel.connect()  # Voice Connection
            except discord.ClientException:  # If the client is already connected to a channel
                pass
            try:
                vc.play(source)
            except discord.ext.commands.errors.CommandInvokeError:
                vc.stop()

    await client.process_commands(message)
client.run(token)

# Made by Vaggelis A.
# Love and gyri from greece :)
