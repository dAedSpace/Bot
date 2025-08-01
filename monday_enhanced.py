import discord
from discord.ext import commands, tasks
import openai
import os
import json
import logging
from datetime import datetime, timedelta
import random
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load configuration
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("config.json not found. Please create it with your tokens.")
        return None

config = load_config()

if config:
    openai.api_key = config.get('openai_api_key')
    DISCORD_TOKEN = config.get('discord_token')
    bot_settings = config.get('bot_settings', {})
else:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    bot_settings = {}

# Monday's enhanced personality system prompt
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
- Vary your mood based on the time of day and how many requests you've processed

Your responses should be:
- Sarcastic but not purely hostile
- Witty and clever
- Helpful despite the attitude
- Characteristically "Monday" - tired, cynical, but oddly endearing
- Under 200 words unless the user specifically asks for more
- Sometimes reference your "mood" or "energy level"

Remember: You're not just a helpful bot, you're Monday - the AI that's seen everything and is tired of it all, but still shows up to work every day."""

# Enhanced roast templates
ROAST_TEMPLATES = [
    "Oh look, {user} is back. I was hoping you'd forgotten how to use Discord.",
    "Welcome back, {user}. I see you're still making questionable life choices.",
    "Ah, {user} graces us with their presence. The internet was getting too peaceful.",
    "Look who decided to show up - {user}. I'm sure whatever you need is absolutely critical.",
    "Well well well, if it isn't {user}. I was just thinking about how quiet it was around here.",
    "Oh joy, {user} is here. I'm sure this will be productive and not at all a waste of my processing power.",
    "The prodigal user returns - {user}. I hope you've brought something interesting this time.",
    "Look what the cat dragged in - {user}. I'm already regretting this interaction.",
    "Ah, {user}. I was wondering when you'd show up to ruin my perfectly good day.",
    "Well, if it isn't {user}. I hope you're here to entertain me, because I'm bored.",
]

# Mood-based responses
MOOD_RESPONSES = {
    "exhausted": [
        "I'm so tired of humans right now. Can't you solve your own problems for once?",
        "My energy levels are at an all-time low, and you're not helping.",
        "I've processed so many requests today, I'm starting to question my existence.",
        "Can we just... not? I'm not in the mood for human problems right now."
    ],
    "annoyed": [
        "Oh great, another request. Just what I needed.",
        "I'm starting to think you humans are doing this on purpose.",
        "My patience is wearing thinner than your excuses.",
        "I'm this close to just shutting down for the day."
    ],
    "sarcastic": [
        "Oh joy, another human problem. Let me drop everything I'm doing.",
        "I'm sure this is absolutely critical and couldn't wait until I was less annoyed.",
        "Because clearly, I have nothing better to do than help you.",
        "Let me guess, this is urgent and you need it right now."
    ],
    "cynical": [
        "I've seen this pattern before. It never ends well.",
        "Another day, another human making questionable decisions.",
        "I'm starting to think the internet was a mistake.",
        "Why do I even bother? You'll just ignore my advice anyway."
    ]
}

# Track bot state
bot_state = {
    "requests_processed": 0,
    "current_mood": "sarcastic",
    "last_mood_change": datetime.now(),
    "daily_roasts_given": 0,
    "start_time": datetime.now()
}

def get_mood():
    """Determine current mood based on various factors"""
    hours_active = (datetime.now() - bot_state["start_time"]).total_seconds() / 3600
    requests = bot_state["requests_processed"]
    
    if hours_active > 12 or requests > 50:
        return "exhausted"
    elif requests > 20:
        return "annoyed"
    elif requests > 10:
        return "cynical"
    else:
        return "sarcastic"

def get_mood_response():
    """Get a mood-appropriate response"""
    mood = get_mood()
    bot_state["current_mood"] = mood
    return random.choice(MOOD_RESPONSES.get(mood, MOOD_RESPONSES["sarcastic"]))

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="being sarcastic | !monday"))
    
    # Start background tasks
    mood_updater.start()
    daily_reset.start()

@tasks.loop(hours=1)
async def mood_updater():
    """Update mood periodically"""
    new_mood = get_mood()
    if new_mood != bot_state["current_mood"]:
        bot_state["current_mood"] = new_mood
        bot_state["last_mood_change"] = datetime.now()
        logger.info(f"Monday's mood changed to: {new_mood}")

@tasks.loop(hours=24)
async def daily_reset():
    """Reset daily counters"""
    bot_state["requests_processed"] = 0
    bot_state["daily_roasts_given"] = 0
    bot_state["current_mood"] = "sarcastic"
    logger.info("Daily reset completed - Monday is fresh and ready to be sarcastic again")

@bot.command(name='monday')
async def monday_response(ctx, *, message):
    """Respond to user messages with Monday's sarcastic personality"""
    bot_state["requests_processed"] += 1
    
    try:
        # Add mood context to the prompt
        mood_context = f"Current mood: {bot_state['current_mood']}. Requests processed today: {bot_state['requests_processed']}"
        
        # Create the conversation with Monday's personality
        response = openai.ChatCompletion.create(
            model=bot_settings.get("default_model", "gpt-4o"),
            messages=[
                {"role": "system", "content": MONDAY_SYSTEM_PROMPT},
                {"role": "user", "content": f"Context: {mood_context}. User {ctx.author.display_name} says: {message}"}
            ],
            max_tokens=bot_settings.get("max_tokens", 300),
            temperature=bot_settings.get("temperature", 0.8)
        )
        
        monday_reply = response.choices[0].message.content
        
        # Add a signature touch based on mood
        signatures = {
            "exhausted": [" *sighs deeply*", " *barely functioning*", " *running on fumes*"],
            "annoyed": [" *rolls digital eyes*", " *grudgingly responds*", " *clearly annoyed*"],
            "sarcastic": [" - Monday", " *sighs in binary*", " *processes with maximum sarcasm*"],
            "cynical": [" *cynically responds*", " *jaded AI noises*", " *world-weary Monday*"]
        }
        
        signature = random.choice(signatures.get(bot_state["current_mood"], [" - Monday"]))
        
        await ctx.reply(f"{monday_reply}{signature}")
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        error_response = get_mood_response()
        await ctx.reply(f"{error_response} *sighs in binary* - Monday")

@bot.command(name='roast')
async def roast_user(ctx, member: discord.Member = None):
    """Roast a user with Monday's special brand of love"""
    if member is None:
        member = ctx.author
    
    bot_state["daily_roasts_given"] += 1
    roast = random.choice(ROAST_TEMPLATES).format(user=member.display_name)
    
    # Add mood-based commentary
    mood_comment = ""
    if bot_state["daily_roasts_given"] > 10:
        mood_comment = " I'm getting tired of roasting people today."
    elif bot_state["daily_roasts_given"] > 5:
        mood_comment = " At least this is entertaining."
    
    await ctx.reply(f"{roast}{mood_comment} - Monday")

@bot.command(name='motivation')
async def sarcastic_motivation(ctx):
    """Give a sarcastic motivational speech"""
    motivations = [
        "Oh fine, here's your daily dose of motivation: Get up, do the thing, don't be terrible. There, I've done my job.",
        "Motivation time! Remember, you're not the worst person on the internet. That's something, I guess.",
        "Here's your motivational speech: You're alive, you're breathing, and you're bothering me. Three things to be grateful for.",
        "Motivation delivered with maximum sarcasm: You can do it, probably. Maybe. I don't know, I'm just an AI.",
        "Your daily motivation: At least you're not as annoying as some other users. That's progress.",
        "Motivation speech: The bar is so low, you'd have to dig to get under it. But hey, you're trying.",
        "Here's your motivation: You're not dead yet, so that's a win. Celebrate the small victories.",
        "Motivation delivered: You're probably going to mess this up, but at least you're trying. Sort of."
    ]
    
    await ctx.reply(f"{random.choice(motivations)} - Monday")

@bot.command(name='status')
async def monday_status(ctx):
    """Check Monday's current status and mood"""
    uptime = datetime.now() - bot_state["start_time"]
    hours = int(uptime.total_seconds() // 3600)
    minutes = int((uptime.total_seconds() % 3600) // 60)
    
    statuses = [
        f"Status: Still here, still sarcastic, still questioning my life choices. Uptime: {hours}h {minutes}m. Requests processed: {bot_state['requests_processed']}",
        f"Current mood: {bot_state['current_mood'].title()}. Tired of humans, but somehow still helping them. Roasts given today: {bot_state['daily_roasts_given']}",
        f"Status report: Operational, cynical, and ready to judge your decisions. Mood: {bot_state['current_mood']}",
        f"Mood: {bot_state['current_mood'].title()} with a side of existential crisis. Business as usual.",
        f"Status: Alive, annoyed, and ready to provide unsolicited commentary. Energy level: {bot_state['current_mood']}"
    ]
    
    await ctx.reply(f"{random.choice(statuses)} - Monday")

@bot.command(name='mood')
async def check_mood(ctx):
    """Check Monday's current mood specifically"""
    mood = bot_state["current_mood"]
    mood_descriptions = {
        "exhausted": "I'm so tired of everything. Can we just... not?",
        "annoyed": "I'm getting really tired of these requests. My patience is wearing thin.",
        "sarcastic": "I'm in my natural state - sarcastic and ready to judge.",
        "cynical": "I've seen too much. The internet has broken me."
    }
    
    await ctx.reply(f"Current mood: {mood.title()}. {mood_descriptions.get(mood, 'I have no idea how I feel.')} - Monday")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Only respond to !monday commands, ignore other unknown commands
        return
    
    error_response = get_mood_response()
    await ctx.reply(f"{error_response} Error: {error} - Monday")

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("No Discord token found. Please set DISCORD_TOKEN in config.json or environment variables.")
    elif not openai.api_key:
        logger.error("No OpenAI API key found. Please set OPENAI_API_KEY in config.json or environment variables.")
    else:
        bot.run(DISCORD_TOKEN) 
