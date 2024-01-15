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

url = "https://www.carousell.sg/categories/cameras-1863/?cameras_type=TYPE_POINT_AND_SHOOT%2CTYPE_DSLR%2CTYPE_MIRRORLESS&searchId=kkZNPc&canChangeKeyword=false&price_end=250&includeSuggestions=false&sort_by=3"
scraper = CarousellScraper(url=url)

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

def create_embed(item):
    embed = discord.Embed(url=f"https://carousell.sg{item['path']}")
    embed.set_image(url=item['image'])
    embed.title=item['title']
    embed.description = f"{item['price']}\n{item['usage']}\n{item['time']}"
    return embed

@tasks.loop(minutes=5)
async def loop(ctx):
    for item in scraper.get_filtered_items():
        embed = create_embed(item)
        await ctx.send(embed=embed)

bot.run(TOKEN)