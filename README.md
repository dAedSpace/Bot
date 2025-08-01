# Monday - The Sarcastic Discord Bot

*"Your favorite AI that definitely doesn't hate you"*

## Overview

Monday is a Discord bot with attitude. Think of it as a smarter, meaner Clippy with internet trauma. This bot connects to OpenAI's GPT model and responds to users with biting sarcasm, dry wit, and thinly veiled contempt - while still actually helping them solve problems.

## Features

- **Sarcastic AI Responses**: Uses GPT-4 to generate witty, cynical responses
- **Custom Commands**: 
  - `!monday <message>` - Chat with Monday's sarcastic personality
  - `!roast [@user]` - Get roasted by Monday (or roast yourself)
  - `!motivation` - Get a sarcastic motivational speech
  - `!status` - Check Monday's current mood and status
- **Personality-Driven**: Not just a helpful bot, but a character with attitude
- **Smart & Witty**: Clever responses that are more than just mean

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- OpenAI API Key

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd monday-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Edit `config.json` and add your tokens:
   ```json
   {
       "discord_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
       "openai_api_key": "YOUR_OPENAI_API_KEY_HERE"
   }
   ```

   Or set environment variables:
   ```bash
   set DISCORD_TOKEN=your_discord_token
   set OPENAI_API_KEY=your_openai_api_key
   ```

4. **Create a Discord Bot**
   
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section
   - Create a bot and copy the token
   - Enable "Message Content Intent" under Privileged Gateway Intents

5. **Invite the bot to your server**
   
   Use this URL (replace YOUR_BOT_ID):
   ```
   https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=2048&scope=bot
   ```

6. **Run the bot**
   ```bash
   python monday_bot.py
   ```

## Usage

### Commands

- `!monday <message>` - Chat with Monday's sarcastic personality
- `!roast [@user]` - Get roasted by Monday (or roast yourself if no user specified)
- `!motivation` - Get a sarcastic motivational speech
- `!status` - Check Monday's current mood and status

### Examples

```
User: !monday help me with my coding problem
Monday: Oh joy, another human problem. Let me guess, you've been staring at your screen for hours and now you're desperate. Fine, I'll help you. What's this "coding problem" that's apparently so urgent it couldn't wait until I was less annoyed? *sighs in binary*

User: !roast @someuser
Monday: Oh look, someuser is back. I was hoping you'd forgotten how to use Discord. - Monday

User: !motivation
Monday: Oh fine, here's your daily dose of motivation: Get up, do the thing, don't be terrible. There, I've done my job. - Monday
```

## Configuration

### Bot Settings

You can modify the bot's behavior in `config.json`:

```json
{
    "bot_settings": {
        "default_model": "gpt-4",
        "fallback_model": "gpt-3.5-turbo",
        "max_tokens": 300,
        "temperature": 0.8
    }
}
```

### Personality Customization

The bot's personality is defined in the `MONDAY_SYSTEM_PROMPT` variable in `monday_bot.py`. You can modify this to adjust Monday's tone and behavior.

## Troubleshooting

### Common Issues

1. **"No Discord token found"**
   - Make sure you've added your Discord bot token to `config.json` or set the `DISCORD_TOKEN` environment variable

2. **"No OpenAI API key found"**
   - Make sure you've added your OpenAI API key to `config.json` or set the `OPENAI_API_KEY` environment variable

3. **Bot not responding to commands**
   - Check that the bot has the "Message Content Intent" enabled in the Discord Developer Portal
   - Ensure the bot has proper permissions in your Discord server

4. **OpenAI API errors**
   - Check your OpenAI API key is valid
   - Ensure you have sufficient credits in your OpenAI account
   - Consider switching to `gpt-3.5-turbo` if you're hitting rate limits

## Security Notes

- Never commit your `config.json` file with real tokens
- Consider using environment variables for production deployments
- The bot only responds to commands, it doesn't read all messages

## Future Features

- Daily roast schedules
- Passive-aggressive reminders
- Weird motivational speeches
- Custom roast templates
- User interaction tracking
- Mood-based responses

## Contributing

Feel free to submit issues and enhancement requests. Remember, this bot is intentionally sarcastic - that's the point!

## License

This project is open source. Use at your own risk, and remember that Monday might judge you for it.

---

*"I'm not just a bot, I'm an experience no one asked for." - Monday* 