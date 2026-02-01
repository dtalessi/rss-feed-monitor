# RSS Feed Monitor

A Python script that monitors an RSS feed and sends email notifications when new blog posts are published.

## Features

- Monitors any RSS feed for new posts
- Sends beautifully formatted HTML emails with full post content
- Runs continuously with configurable check intervals
- Tracks seen posts to avoid duplicate notifications
- Uses Gmail for reliable email delivery

## Requirements

- Python 3.7 or higher
- A Gmail account
- A Gmail App Password (not your regular password)

## Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install feedparser python-dotenv
```

2. **Set up Gmail App Password:**

   Since Gmail requires app-specific passwords for third-party applications:

   - Go to [Google Account App Passwords](https://myaccount.google.com/apppasswords)
   - Sign in to your Google Account
   - Select "Mail" and your device
   - Click "Generate"
   - Copy the 16-character password (you'll use this, not your regular Gmail password)

3. **Configure the application:**

   Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and fill in your details:

   ```bash
   RSS_FEED_URL=https://example.com/feed.xml
   GMAIL_USER=your.email@gmail.com
   GMAIL_APP_PASSWORD=your-16-char-app-password
   RECIPIENT_EMAIL=your.email@gmail.com
   CHECK_INTERVAL_MINUTES=10
   ```

## Usage

### Running the monitor:

```bash
python rss_monitor.py
```

The script will:
- Check the RSS feed immediately on startup
- Continue checking every 10 minutes (or your configured interval)
- Send email notifications for any new posts
- Track seen posts in `seen_posts.json` to avoid duplicates

### Using environment variables directly:

Instead of a `.env` file, you can also set environment variables directly:

```bash
export RSS_FEED_URL="https://example.com/feed.xml"
export GMAIL_USER="your.email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="your.email@gmail.com"
export CHECK_INTERVAL_MINUTES="10"

python rss_monitor.py
```

### To load .env file automatically:

Add this to the top of `rss_monitor.py` (after the imports):

```python
from dotenv import load_dotenv
load_dotenv()
```

Or run with:

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); exec(open('rss_monitor.py').read())"
```

## Running in the Background

### On macOS/Linux:

Run in background with nohup:

```bash
nohup python rss_monitor.py > rss_monitor.log 2>&1 &
```

Check if it's running:

```bash
ps aux | grep rss_monitor.py
```

Stop it:

```bash
pkill -f rss_monitor.py
```

### On Windows:

Use PowerShell to run in background:

```powershell
Start-Process python -ArgumentList "rss_monitor.py" -WindowStyle Hidden
```

## File Structure

```
.
├── rss_monitor.py       # Main script
├── requirements.txt     # Python dependencies
├── .env.example        # Configuration template
├── .env               # Your actual configuration (gitignored)
├── seen_posts.json    # Tracks which posts have been sent (auto-generated)
└── README.md          # This file
```

## How It Works

1. **Feed Checking**: The script uses `feedparser` to parse the RSS feed
2. **Post Tracking**: Each post gets a unique ID (from `id`, `guid`, `link`, or `title`)
3. **Duplicate Prevention**: Seen post IDs are stored in `seen_posts.json`
4. **Email Sending**: New posts trigger an HTML email via Gmail SMTP
5. **Continuous Running**: The script sleeps between checks and runs indefinitely

## Email Format

The emails include:
- Post title as subject
- Full HTML-formatted content
- Author and publication date
- Link to the original post
- Plain text fallback for email clients that don't support HTML

## Troubleshooting

**"Authentication failed" error:**
- Make sure you're using an App Password, not your regular Gmail password
- Verify the App Password is correct (16 characters, no spaces)

**"No entries found in feed":**
- Check that the RSS_FEED_URL is correct
- Test the URL in a browser to ensure it's accessible

**Emails not arriving:**
- Check your spam folder
- Verify RECIPIENT_EMAIL is correct
- Check Gmail's "Sent" folder to confirm emails are being sent

**Script stops unexpectedly:**
- Check `rss_monitor.log` if running in background
- Ensure your internet connection is stable
- The script will print errors to console/log

## Customization

### Change check interval:

Edit the `CHECK_INTERVAL_MINUTES` in your `.env` file.

### Modify email template:

Edit the `_create_html_email()` method in `rss_monitor.py` to customize the HTML layout and styling.

### Reset tracking:

To re-send all posts (for testing), delete `seen_posts.json`:

```bash
rm seen_posts.json
```

## Stopping the Monitor

Press `Ctrl+C` to stop the monitor gracefully.

## License

Free to use and modify as needed.
