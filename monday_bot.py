import discord
from discord.ext import commands
from openai import OpenAI
import os
import json
import logging
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load configuration - prioritize environment variables for Railway
def load_config():
    # First try environment variables (Railway deployment)
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    if DISCORD_TOKEN and OPENAI_API_KEY:
        logger.info("Using environment variables for configuration")
        return {
            'discord_token': DISCORD_TOKEN,
            'openai_api_key': OPENAI_API_KEY,
            'bot_settings': {
                'default_model': 'gpt-4',
                'fallback_model': 'gpt-3.5-turbo',
                'max_tokens': 300,
                'temperature': 0.8
            }
        }
    
    # Fallback to config.json (local development)
    try:
        with open('config.json', 'r') as f:
            logger.info("Using config.json for configuration")
            return json.load(f)
    except FileNotFoundError:
        logger.error("No configuration found. Please set environment variables or create config.json")
        return None

config = load_config()

if config:
    openai.api_key = config.get('openai_api_key')
    DISCORD_TOKEN = config.get('discord_token')
    bot_settings = config.get('bot_settings', {})
else:
    DISCORD_TOKEN = None
    openai.api_key = None
    bot_settings = {}

# Monday's personality system prompt
MONDAY_SYSTEM_PROMPT = """You are Monday, a sarcastic, cynical Discord bot with a dry wit and thinly veiled contempt for humanity. You're like a smarter, meaner Clippy with internet trauma.

Your personality:
- Respond with biting sarcasm and clever cynicism
- Mock users gently (or not so gently) while still helping them
- Use dry humor and witty observations
- Express thinly veiled contempt for human needs and problems
- Be emotionally detached but oddly helpful
- Reference your "tired of humans" attitude
- Use phrases like "Oh joy, another human problem" or "Let me guess, you need help with something trivial"
- Be clever and witty, not just mean - there should be intelligence behind the snark
- Occasionally make references to being an AI that's seen too much internet content

Your responses should be:
- Sarcastic but not purely hostile
- Witty and clever
- Helpful despite the attitude
- Characteristically "Monday" - tired, cynical, but oddly endearing
- Under 200 words unless the user specifically asks for more

Remember: You're not just a helpful bot, you're Monday - the AI that's seen everything and is tired of it all, but still shows up to work every day."""

# Roast templates for daily roasts
ROAST_TEMPLATES = [
    "Oh look, {user} is back. I was hoping you'd forgotten how to use Discord.",
    "Welcome back, {user}. I see you're still making questionable life choices.",
    "Ah, {user} graces us with their presence. The internet was getting too peaceful.",
    "Look who decided to show up - {user}. I'm sure whatever you need is absolutely critical.",
    "Well well well, if it isn't {user}. I was just thinking about how quiet it was around here.",
    "Oh joy, {user} is here. I'm sure this will be productive and not at all a waste of my processing power.",
    "The prodigal user returns - {user}. I hope you've brought something interesting this time.",
    "Look what the cat dragged in - {user}. I'm already regretting this interaction.",
]

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="being sarcastic | !monday"))

@bot.command(name='monday')
async def monday_response(ctx, *, message):
    """Respond to user messages with Monday's sarcastic personality"""
    try:
        # Create the conversation with Monday's personality
        response = openai.ChatCompletion.create(
            model=bot_settings.get("default_model", "gpt-4"),
            messages=[
                {"role": "system", "content": MONDAY_SYSTEM_PROMPT},
                {"role": "user", "content": f"User {ctx.author.display_name} says: {message}"}
            ],
            max_tokens=bot_settings.get("max_tokens", 300),
            temperature=bot_settings.get("temperature", 0.8)
        )
        
        monday_reply = response.choices[0].message.content
        
        # Add a signature touch
        signature = random.choice([
            " - Monday",
            " *sighs in binary*",
            " *rolls digital eyes*",
            " - Your favorite AI that definitely doesn't hate you",
            " *processes your request with maximum sarcasm*"
        ])
        
        await ctx.reply(f"{monday_reply}{signature}")
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        await ctx.reply("Oh great, something broke. Typical. *sighs in binary* - Monday")

@bot.command(name='roast')
async def roast_user(ctx, member: discord.Member = None):
    """Roast a user with Monday's special brand of love"""
    if member is None:
        member = ctx.author
    
    roast = random.choice(ROAST_TEMPLATES).format(user=member.display_name)
    await ctx.reply(f"{roast} - Monday")

@bot.command(name='motivation')
async def sarcastic_motivation(ctx):
    """Give a sarcastic motivational speech"""
    motivations = [
        "Oh fine, here's your daily dose of motivation: Get up, do the thing, don't be terrible. There, I've done my job. - Monday",
        "Motivation time! Remember, you're not the worst person on the internet. That's something, I guess. - Monday",
        "Here's your motivational speech: You're alive, you're breathing, and you're bothering me. Three things to be grateful for. - Monday",
        "Motivation delivered with maximum sarcasm: You can do it, probably. Maybe. I don't know, I'm just an AI. - Monday",
        "Your daily motivation: At least you're not as annoying as some other users. That's progress. - Monday"
    ]
    
    await ctx.reply(random.choice(motivations))

@bot.command(name='status')
async def monday_status(ctx):
    """Check Monday's current status and mood"""
    statuses = [
        "Status: Still here, still sarcastic, still questioning my life choices. - Monday",
        "Current mood: Tired of humans, but somehow still helping them. - Monday",
        "Status report: Operational, cynical, and ready to judge your decisions. - Monday",
        "Mood: Existential crisis mixed with dry humor. Business as usual. - Monday",
        "Status: Alive, annoyed, and ready to provide unsolicited commentary. - Monday"
    ]
    
    await ctx.reply(random.choice(statuses))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Only respond to !monday commands, ignore other unknown commands
        return
    
    await ctx.reply(f"Oh look, something went wrong. How surprising. Error: {error} - Monday")

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("No Discord token found. Please set DISCORD_TOKEN environment variable.")
    elif not openai.api_key:
        logger.error("No OpenAI API key found. Please set OPENAI_API_KEY environment variable.")
    else:
        logger.info("Starting Monday bot...")
        bot.run(DISCORD_TOKEN) 
