#!/usr/bin/env python3
import signal, os, sys
import discord
from discord.ext import commands
from bot_actions import start_server, get_status, get_number_of_players
from load_conf import load_yaml
import facts as mcfacts 
import AternosParsingError

conf = load_yaml("/home/jracaud/.discord/bots/aternos/conf.yaml")
BOT_TOKEN = conf['bot_token']

bot = commands.Bot(command_prefix="!")
facts = mcfacts.load_facts()

@bot.event
async def on_ready():
    print('We have logged in as {0.user.name}#{0.user.id}'.format(bot))

@bot.command(help="Start the server.")
async def start(ctx):
    try:
        if get_status() == "Offline":
            await ctx.send("Starting the server")
            await start_server(ctx)
        else:
            await ctx.send("Server already running")
    except AternosParsingError as e:
        print("Error starting the server: {0}".format(e.reason))
        await ctx.send("[Error] Couldn't start the server: {0}.".format(e.reason)) 
    except Exception as e:
        print("Unkown error {0}".format(e))
        await ctx.send("[Error] Unknown error: {0}. Please contact my developer for debugging".format(e))

@bot.command(help="Gives the server's status: [Offline/Online].")
async def status(ctx):
    await ctx.send("The server is {0}".format(get_status()))

@bot.command(help="Gives the numbers of players on the server and total capacity.")
async def players(ctx):
    await ctx.send("There are {0} players on the server".format(get_number_of_players()))

@bot.command(help="Gives a fact about minecraft")
async def fact(ctx):
    (key, fact) = mcfacts.get_random_fact_with_number(facts)
    await ctx.send("Fact #{0}: {1}".format(key, fact))

def signal_handler(signum, frame):
    print("Received signal {0}. Terminating now".format(signum))
    bot.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
bot.run(BOT_TOKEN)
