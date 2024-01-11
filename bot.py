import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from request import CarousellScraper

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True # We want to see what a user has written
intents.members = True # see members' actions
intents.guilds = True # access to guild's stuff
intents.emojis_and_stickers = True


# Command prefix (e.g. "!" for !ping)
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

scraper = CarousellScraper()

@bot.command()
async def start(ctx):
    if not loop.is_running():
        await ctx.send("Starting Bot!")
        loop.start(ctx)
    else:
        await ctx.send("Bot already running!")

@bot.command()
async def stop(ctx):
    if loop.is_running():
        await ctx.send("Stopping Bot!")
        loop.cancel()
    else:
        await ctx.send("Bot is not running!")

@bot.command()
async def status(ctx):
    if loop.is_running():
        await ctx.send("Bot is running!")
    else:
        await ctx.send("Bot is not running!")

@tasks.loop(seconds=60)
async def loop(ctx):
    # await ctx.send("Checking for listings...")
    for item in scraper.check():
        embed = discord.Embed(url=item['link'])
        embed.set_image(url=item['image'])
        embed.title=item['title']
        embed.description = f"{item['price']}\n{item['usage']}\n{item['time']}"
        await ctx.send(embed=embed)

bot.run(TOKEN)