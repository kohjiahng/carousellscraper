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

loops = {}

@bot.command()
async def start(ctx, url=None):
    if not url:
        url = "https://www.carousell.sg/categories/cameras-1863/?cameras_type=TYPE_POINT_AND_SHOOT%2CTYPE_DSLR%2CTYPE_MIRRORLESS&searchId=kkZNPc&canChangeKeyword=false&price_end=250&includeSuggestions=false&sort_by=3"
    channel_id = ctx.channel.id
    if channel_id not in loops:
        await ctx.send("Starting Bot!")

        scraper = CarousellScraper(url=url)
        loop = create_loop(ctx, scraper)
        loops[channel_id] = loop
        loop.start()
    else:
        await ctx.send("Bot already running!")

@bot.command()
async def stop(ctx):
    channel_id = ctx.channel.id
    if channel_id in loops:
        await ctx.send("Stopping Bot!")
        loops[channel_id].cancel()
        del loops[channel_id]
    else:
        await ctx.send("Bot is not running!")

@bot.command()
async def status(ctx):
    channel_id = ctx.channel.id 
    if channel_id in loops:
        await ctx.send("Bot is running!")
    else:
        await ctx.send("Bot is not running!")

def create_embed(item):
    embed = discord.Embed(url=f"https://carousell.sg{item['path']}")
    embed.set_image(url=item['image'])
    embed.title=item['title']
    embed.description = f"{item['price']}\n{item['usage']}\n{item['time']}"
    return embed

def create_loop(ctx, scraper):
    @tasks.loop(minutes=5)
    async def loop():
        for item in scraper.get_filtered_items():
            embed = create_embed(item)
            await ctx.send(embed=embed)
    return loop

bot.run(TOKEN)