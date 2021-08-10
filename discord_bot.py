import logging
import os 

from dotenv import load_dotenv
from discord.ext import commands
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

logger = logging.getLogger(__name__)

# load env
load_dotenv('.env')
linegroup = os.getenv("LINEGROUP")
line_bot_api = LineBotApi(os.getenv("CHANNEL_TOKEN"))
discordtoken = os.getenv("DISCORD_TOKEN")

# discord bot
discordbot = commands.Bot(command_prefix = "!")

# define global env
line = True

@discordbot.event
async def on_message(message):
    if message.author == discordbot.user:
        logger.debug("message from self")
        return
    if message.content[0] == "!":
        logger.debug("discord command")
        await discordbot.process_commands(message)
        return 
    if not line:
        logger.debug("send to line turn off")
        return

    reponse = (
            f"🖥️ CHANNEL: {message.channel}\n"
            f"🟢 FROM: {message.author}\n"
            f"💬 {message.content}"
        )
    try:
        line_bot_api.push_message(linegroup, TextSendMessage(text=reponse))
    except LineBotApiError as e:
        discordbot.channel.send("Send to line error")

@discordbot.command(
        name = "lineoff",
        help=':For turn off message to line.'
    )
async def lineoff(ctx):
    logger.debug("!lineoff")
    global line

    if line == True:
        line = False
        await ctx.channel.send("Turn off successfull !!")
    else:
        await ctx.channel.send("Line already turn off")

@discordbot.command(
        name = "lineon",
        help=':For turn on message to line.'
    )
async def lineon(ctx):
    logger.debug("!lineon")
    global line

    if line == False:
        line = True
        await ctx.channel.send("Turn on successfull !!")
    else:
        await ctx.channel.send("Line already turn on")


discordbot.run(discordtoken)