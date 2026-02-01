# GitHub Actions Setup Guide

This guide will help you set up the RSS monitor to run 24/7 on GitHub Actions for free.

## What You'll Get

- RSS feed checked every 10 minutes, 24/7
- Runs on GitHub's servers (not your computer)
- Completely free for public repositories
- Automatic email notifications for new posts

## Prerequisites

- A GitHub account (create one at https://github.com/join if needed)
- Git installed on your computer

## Setup Steps

### 1. Stop the Local LaunchAgent

First, stop the local version since we'll be using GitHub Actions instead:

```bash
cd /Users/dominique.alessi/Desktop/dom-coding-projects
./setup_autostart.sh uninstall
```

### 2. Initialize Git Repository

```bash
cd /Users/dominique.alessi/Desktop/dom-coding-projects
git init
git add .
git commit -m "Initial commit: RSS feed monitor"
```

### 3. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `rss-feed-monitor` (or any name you prefer)
3. **Important:** Set visibility to **Public** (private repos have limited free minutes)
4. DO NOT initialize with README, .gitignore, or license (we already have files)
5. Click "Create repository"

### 4. Push Code to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/rss-feed-monitor.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 5. Set Up GitHub Secrets

Your credentials need to be stored securely in GitHub. Go to your repository on GitHub:

1. Click "Settings" tab
2. In the left sidebar, click "Secrets and variables" → "Actions"
3. Click "New repository secret" for each of these:

**Secret 1: RSS_FEED_URL**
- Name: `RSS_FEED_URL`
- Value: `https://crossfitsouthbrooklyn.com/feed/`

**Secret 2: GMAIL_USER**
- Name: `GMAIL_USER`
- Value: `dtalessi@gmail.com`

**Secret 3: GMAIL_APP_PASSWORD**
- Name: `GMAIL_APP_PASSWORD`
- Value: `gfiujgsmnnkzaval`

**Secret 4: RECIPIENT_EMAIL**
- Name: `RECIPIENT_EMAIL`
- Value: `dtalessi@gmail.com`

### 6. Enable GitHub Actions

1. In your repository, click the "Actions" tab
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. You should see the "RSS Feed Monitor" workflow

### 7. Test the Workflow

Run it manually to make sure everything works:

1. Click on "RSS Feed Monitor" workflow
2. Click "Run workflow" dropdown
3. Click the green "Run workflow" button
4. Wait a few seconds and refresh the page
5. Click on the workflow run to see the logs

You should see:
- "First run - marking X existing posts as seen"
- "Setup complete! Future posts will trigger email notifications."

### 8. Verify It's Working

The workflow is now set to run every 10 minutes automatically. To verify:

1. Go to the "Actions" tab
2. You'll see workflow runs appearing every 10 minutes
3. Click on any run to see the logs
4. You should see "No new posts" (until a new post is published)

When a new post is published, you'll get an email!

## Monitoring

### View Workflow Runs
- Go to your repository → "Actions" tab
- See all past runs and their status

### View Logs
- Click on any workflow run
- Click "check-feed" job
- See detailed logs of what happened

### Manual Trigger
- Actions tab → RSS Feed Monitor → Run workflow
- Useful for testing or checking immediately

## Troubleshooting

### "Error: Missing required environment variables"
- Make sure all 4 secrets are set correctly in Settings → Secrets

### "Authentication failed"
- Double-check your GMAIL_APP_PASSWORD secret
- Make sure it's the app password, not your regular Gmail password

### Workflow not running
- Check that the workflow file is in `.github/workflows/rss-monitor.yml`
- Make sure GitHub Actions is enabled for your repository
- Public repos have unlimited action minutes; private repos have 2,000/month

### Want to change check frequency?
Edit `.github/workflows/rss-monitor.yml` and change this line:
```yaml
- cron: '*/10 * * * *'  # Every 10 minutes
```

To:
```yaml
- cron: '*/30 * * * *'  # Every 30 minutes
- cron: '0 * * * *'     # Every hour
- cron: '0 */2 * * *'   # Every 2 hours
```

Then commit and push the change.

## Stopping the Monitor

To stop the automated checks:

1. Go to repository Settings
2. Scroll down to "Danger Zone"
3. Click "Disable Actions" for this repository

Or just delete the `.github/workflows/rss-monitor.yml` file.

## Cost

- **Public repository:** Completely free, unlimited minutes
- **Private repository:** 2,000 minutes/month free (about 13 days of 10-minute checks)

That's why we recommend making it public!

## Security Note

Your `.env` file is in `.gitignore` so it won't be pushed to GitHub. Your credentials are only stored in GitHub Secrets, which are encrypted and not visible to anyone (including you, once set).
