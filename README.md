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

## Adding more email recipients

The `RECIPIENT_EMAIL` secret accepts a comma-separated list of addresses, so you can notify multiple people without changing any code.

**Steps:**

1. Go to **Settings → Secrets and variables → Actions** in your repo
2. Click the pencil icon next to `RECIPIENT_EMAIL`
3. Replace the single address with a comma-separated list:

```
you@example.com, teammate@example.com, another@example.com
```

4. Click **Save secret**

All addresses listed will receive the same notification email the next time a new post is detected. No code changes or redeployment needed.

> **Privacy:** Recipients are sent as BCC, so no one in the list can see the other addresses.

## Limitations

- **GitHub Actions cron scheduling is not exact.** GitHub does not guarantee that scheduled workflows fire precisely on time — during periods of high load, runs can be delayed by several minutes or more. The monitor is designed for near-real-time alerts, not second-level precision.
- **GitHub may pause scheduled workflows on inactive repos.** If a repository has no commits or other activity for 60 days, GitHub automatically disables scheduled workflows. To re-enable, go to the **Actions** tab and click **Enable**.
- **Gmail sending limits.** Free Gmail accounts are capped at 500 outbound emails per day via SMTP. If the blog is very active or you have many recipients, you could hit this limit. Google Workspace accounts have a higher limit (2,000/day).
- **All recipients are BCC'd.** No recipient can see the other addresses in the list.
- **The `RECIPIENT_EMAIL` secret has a character limit.** GitHub Actions secrets can store up to 48 KB, so the comma-separated list can be very long in practice, but it is not unlimited.
- **No unsubscribe mechanism.** There is no built-in way for recipients to opt out. To remove someone, you must edit the `RECIPIENT_EMAIL` secret manually.
- **One RSS feed per workflow.** The current setup monitors a single feed (`RSS_FEED_URL`). To monitor additional feeds, duplicate the workflow file and set separate secrets for each.

## Changing the check frequency

Edit `.github/workflows/rss-monitor.yml` in the repo and update the cron expression:

```yaml
- cron: '*/10 * * * *'   # every 10 minutes (current)
- cron: '*/30 * * * *'   # every 30 minutes
- cron: '0 * * * *'      # every hour
```
