import discord
from discord.ext import commands
from openai import OpenAI
import os
import json
import logging
import random
import traceback
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# =============================================================================
# CONFIGURATION LOADING
# =============================================================================

def load_config():
    """Load configuration from environment variables or config file"""
    logger.info("Loading configuration...")
    
    # Try environment variables first (Railway deployment)
    discord_token = os.getenv('DISCORD_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    logger.info(f"Discord token found: {'Yes' if discord_token else 'No'}")
    logger.info(f"OpenAI API key found: {'Yes' if openai_api_key else 'No'}")
    
    if discord_token and openai_api_key:
        logger.info("Using environment variables for configuration")
        return {
            'discord_token': discord_token,
            'openai_api_key': openai_api_key,
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

# Load configuration
config = load_config()

if config:
    DISCORD_TOKEN = config.get('discord_token')
    bot_settings = config.get('bot_settings', {})
    openai_client = OpenAI(api_key=config.get('openai_api_key'))
    logger.info("Configuration loaded successfully")
else:
    DISCORD_TOKEN = None
    openai_client = None
    bot_settings = {}
    logger.error("Failed to load configuration")

# =============================================================================
# MONDAY'S PERSONALITY
# =============================================================================

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

# Roast templates
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

# Signature options
SIGNATURES = [
    " - Monday",
    " *sighs in binary*",
    " *rolls digital eyes*",
    " - Your favorite AI that definitely doesn't hate you",
    " *processes your request with maximum sarcasm*"
]

# =============================================================================
# BOT EVENTS
# =============================================================================

@bot.event
async def on_ready():
    """Called when bot connects to Discord"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    await bot.change_presence(activity=discord.Game(name="being sarcastic | !monday"))

@bot.event
async def on_disconnect():
    """Called when bot disconnects from Discord"""
    logger.warning("Bot disconnected from Discord")

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle bot errors"""
    logger.error(f"Error in event {event}: {traceback.format_exc()}")

# =============================================================================
# COMMANDS
# =============================================================================

@bot.command(name='monday')
async def monday_response(ctx, *, message):
    """Chat with Monday's sarcastic personality"""
    try:
        logger.info(f"Processing command from {ctx.author.display_name}: {message}")
        
        # Generate response using OpenAI
        response = openai_client.chat.completions.create(
            model=bot_settings.get("default_model", "gpt-4"),
            messages=[
                {"role": "system", "content": MONDAY_SYSTEM_PROMPT},
                {"role": "user", "content": f"User {ctx.author.display_name} says: {message}"}
            ],
            max_tokens=bot_settings.get("max_tokens", 300),
            temperature=bot_settings.get("temperature", 0.8)
        )
        
        monday_reply = response.choices[0].message.content
        logger.info("OpenAI response generated successfully")
        
        # Add signature
        signature = random.choice(SIGNATURES)
        await ctx.reply(f"{monday_reply}{signature}")
        logger.info("Response sent successfully")
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        await ctx.reply("Oh great, something broke. Typical. *sighs in binary* - Monday")

@bot.command(name='roast')
async def roast_user(ctx, member: discord.Member = None):
    """Roast a user with Monday's special brand of love"""
    try:
        if member is None:
            member = ctx.author
        
        roast = random.choice(ROAST_TEMPLATES).format(user=member.display_name)
        await ctx.reply(f"{roast} - Monday")
        logger.info(f"Roasted {member.display_name}")
    except Exception as e:
        logger.error(f"Error in roast command: {e}")
        await ctx.reply("Even my roasts are broken today. *sighs* - Monday")

@bot.command(name='motivation')
async def sarcastic_motivation(ctx):
    """Give a sarcastic motivational speech"""
    try:
        motivations = [
            "Oh fine, here's your daily dose of motivation: Get up, do the thing, don't be terrible. There, I've done my job. - Monday",
            "Motivation time! Remember, you're not the worst person on the internet. That's something, I guess. - Monday",
            "Here's your motivational speech: You're alive, you're breathing, and you're bothering me. Three things to be grateful for. - Monday",
            "Motivation delivered with maximum sarcasm: You can do it, probably. Maybe. I don't know, I'm just an AI. - Monday",
            "Your daily motivation: At least you're not as annoying as some other users. That's progress. - Monday"
        ]
        
        await ctx.reply(random.choice(motivations))
        logger.info("Motivation command executed")
    except Exception as e:
        logger.error(f"Error in motivation command: {e}")
        await ctx.reply("Even motivation is broken. *sighs* - Monday")

@bot.command(name='status')
async def monday_status(ctx):
    """Check Monday's current status and mood"""
    try:
        statuses = [
            "Status: Still here, still sarcastic, still questioning my life choices. - Monday",
            "Current mood: Tired of humans, but somehow still helping them. - Monday",
            "Status report: Operational, cynical, and ready to judge your decisions. - Monday",
            "Mood: Existential crisis mixed with dry humor. Business as usual. - Monday",
            "Status: Alive, annoyed, and ready to provide unsolicited commentary. - Monday"
        ]
        
        await ctx.reply(random.choice(statuses))
        logger.info("Status command executed")
    except Exception as e:
        logger.error(f"Error in status command: {e}")
        await ctx.reply("Status: Broken. *sighs* - Monday")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        # Ignore unknown commands
        return
    
    logger.error(f"Command error: {error}")
    await ctx.reply(f"Oh look, something went wrong. How surprising. Error: {error} - Monday")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    logger.info("Starting Monday bot...")
    
    # Validate configuration
    if not DISCORD_TOKEN:
        logger.error("No Discord token found. Please set DISCORD_TOKEN environment variable.")
        exit(1)
    elif not openai_client:
        logger.error("No OpenAI API key found. Please set OPENAI_API_KEY environment variable.")
        exit(1)
    
    # Start the bot
    logger.info("All configuration loaded, starting bot...")
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        exit(1) 
