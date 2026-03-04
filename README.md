# CFSBK Blog Monitor

Monitors the [CrossFit South Brooklyn blog](https://crossfitsouthbrooklyn.com) RSS feed and sends an email notification whenever a new post is published. Runs automatically every 10 minutes via GitHub Actions.

## How it works

1. GitHub Actions triggers `rss_monitor_once.py` on a cron schedule (`*/10 * * * *`)
2. The script fetches the CFSBK RSS feed and compares entries against `seen_posts.json` (committed in the repo) to identify new posts
3. New posts trigger an HTML-formatted email via Gmail SMTP
4. `seen_posts.json` is committed back to the repo after each run so state persists between invocations
5. On the very first run, all existing posts are marked as seen without sending any emails — only posts published after setup generate notifications

## Repository secrets required

Set these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `RSS_FEED_URL` | `https://crossfitsouthbrooklyn.com/feed/` |
| `GMAIL_USER` | Gmail address to send from |
| `GMAIL_APP_PASSWORD` | [Gmail App Password](https://myaccount.google.com/apppasswords) (not your regular password) |
| `RECIPIENT_EMAIL` | Email address to receive notifications |

## Files

```
├── rss_monitor_once.py   # Script run by GitHub Actions
├── requirements.txt      # Python dependencies (feedparser)
├── GITHUB_SETUP.md       # Step-by-step GitHub Actions setup guide
└── README.md
```

## Changing the check frequency

Edit `.github/workflows/rss-monitor.yml` in the repo and update the cron expression:

```yaml
- cron: '*/10 * * * *'   # every 10 minutes (current)
- cron: '*/30 * * * *'   # every 30 minutes
- cron: '0 * * * *'      # every hour
```
