#!/usr/bin/env python3
import os
import requests
import discord
from discord.ext import commands
from connect_and_launch import start_server
from lxml import html

conf = load_yaml("conf.yaml")
BOT_TOKEN = conf['bot_token']
SERVER = conf['host']['server']

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('We have logged in as {0.user.name}#{0.user.id}'.format(bot))

@bot.command()
async def start(ctx):
    if get_status == "Offline":
        await ctx.send("Starting the server")
        await start_server()
    else:
        await ctx.send("Server already running")

@bot.command()
async def status(ctx):
    await ctx.send("The server is {0}".format(get_status()))

@bot.command()
async def status(ctx):
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

bot.run(BOT_TOKEN)
