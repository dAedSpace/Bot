# Monday Bot - Railway Deployment Guide

## Prerequisites
- GitHub account
- Railway account (free at [railway.app](https://railway.app))
- Discord Bot Token
- OpenAI API Key

## Step 1: Prepare Your Repository

1. **Create a GitHub repository** for your Monday bot
2. **Upload all files** to the repository:
   - `monday_bot.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `railway.json`
   - `README.md`
   - `.gitignore`

## Step 2: Set Up Railway

1. **Go to [Railway.app](https://railway.app)** and sign in with GitHub
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your Monday bot repository**
5. **Click "Deploy"**

## Step 3: Configure Environment Variables

1. **In your Railway project dashboard**, go to the "Variables" tab
2. **Add these environment variables**:

```
DISCORD_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Click "Add"** for each variable
4. **Redeploy** your project (Railway will automatically redeploy when you add variables)

## Step 4: Verify Deployment

1. **Check the logs** in Railway dashboard
2. **Look for**: "Monday bot has connected to Discord!"
3. **If you see errors**, check:
   - Environment variables are set correctly
   - Discord bot token is valid
   - OpenAI API key is valid

## Step 5: Test Your Bot

1. **Go to your Discord server**
2. **Try the commands**:
   - `!monday hello`
   - `!roast`
   - `!motivation`
   - `!status`

## Troubleshooting

### Bot not responding?
- Check Railway logs for errors
- Verify Discord bot has proper permissions
- Ensure "Message Content Intent" is enabled in Discord Developer Portal

### OpenAI API errors?
- Check your API key is correct
- Ensure you have credits in your OpenAI account
- Consider switching to `gpt-3.5-turbo` in the code if hitting rate limits

### Railway deployment fails?
- Check the logs for build errors
- Ensure all files are in the repository
- Verify `requirements.txt` is correct

## Railway Features

- **Automatic restarts** when the bot crashes
- **Free tier** available
- **Easy scaling** if needed
- **Git integration** for easy updates

## Updating Your Bot

1. **Make changes** to your code
2. **Push to GitHub**
3. **Railway automatically redeploys**

## Cost

- **Free tier**: $5 credit per month
- **Monday bot**: Should use minimal resources
- **Estimated cost**: $0-2/month depending on usage

---

*"Deployed and ready to be sarcastic 24/7" - Monday* 