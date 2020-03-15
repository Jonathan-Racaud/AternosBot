#!/usr/bin/env python3
import signal, os, sys
import requests
import discord
from discord.ext import commands
from connect_and_launch import start_server
from lxml import html
from load_conf import load_yaml
import AternosParsingError

conf = load_yaml("/home/jracaud/.discord/bots/aternos/conf.yaml")
BOT_TOKEN = conf['bot_token']
SERVER = conf['host']['server']

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('We have logged in as {0.user.name}#{0.user.id}'.format(bot))

@bot.command()
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

@bot.command()
async def status(ctx):
    await ctx.send("The server is {0}".format(get_status()))

@bot.command()
async def players(ctx):
    await ctx.send("There are {0} players on the server".format(get_number_of_players()))

@bot.command()
async def stop(ctx):
    await ctx.send("I do no know how to stop the server yet!")

def get_status():
    page = requests.get(SERVER)
    tree = html.fromstring(page.content)
    status = tree.xpath('/html/body/div/div[3]/div/div/div[1]/span/text()')
    return status[0]

def get_number_of_players():
    page = requests.get(SERVER)
    tree = html.fromstring(page.content)
    status = tree.xpath('/html/body/div/div[4]/div/div/div/span[1]/text()')
    return status[0]

def signal_handler(signum, frame):
    print("Received signal {0}. Terminating now".format(signum))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
bot.run(BOT_TOKEN)
