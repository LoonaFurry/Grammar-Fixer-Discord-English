import discord
from discord.ext import commands
from language_tool_python import LanguageTool

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up LanguageTool for English
tool_en = LanguageTool('en-US')  # Set language to English (US)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the message contains text
    if not message.content:
        return

    # Get the text from the message
    text = message.content

    # Check for grammar errors
    matches = tool_en.check(text)

    # If there are errors, fix them and send a corrected message
    if len(matches) > 0:
        corrected_text = tool_en.correct(text)
        await message.channel.send(f'Grammar fix: {corrected_text}')

    # Process the message as usual
    await bot.process_commands(message)

@bot.command(name='fix', help='Fix grammar errors in a message')
async def fix(ctx, *, text: str):
    # Check for grammar errors
    matches = tool_en.check(text)

    # If there are errors, fix them and send a corrected message
    if len(matches) > 0:
        corrected_text = tool_en.correct(text)
        await ctx.send(f'Grammar fix: {corrected_text}')
    else:
        await ctx.send('No grammar errors found!')

bot.run('your-discord-token-here')
