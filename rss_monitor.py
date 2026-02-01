#!/usr/bin/env python3
"""
RSS Feed Monitor - Monitors an RSS feed and emails new posts
"""

import feedparser
import smtplib
import time
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from typing import Set, Dict, Any
import html

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use system environment variables


class RSSMonitor:
    def __init__(self, rss_url: str, gmail_user: str, gmail_app_password: str, recipient_email: str):
        """
        Initialize the RSS Monitor

        Args:
            rss_url: URL of the RSS feed to monitor
            gmail_user: Gmail address to send from
            gmail_app_password: Gmail app password (not regular password)
            recipient_email: Email address to send notifications to
        """
        self.rss_url = rss_url
        self.gmail_user = gmail_user
        self.gmail_app_password = gmail_app_password
        self.recipient_email = recipient_email
        self.seen_file = Path("seen_posts.json")
        self.seen_posts = self._load_seen_posts()

    def _load_seen_posts(self) -> Set[str]:
        """Load previously seen post IDs from file"""
        if self.seen_file.exists():
            try:
                with open(self.seen_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('seen_ids', []))
            except Exception as e:
                print(f"Error loading seen posts: {e}")
                return set()
        return set()

    def _save_seen_posts(self):
        """Save seen post IDs to file"""
        try:
            with open(self.seen_file, 'w') as f:
                json.dump({
                    'seen_ids': list(self.seen_posts),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving seen posts: {e}")

    def _get_post_id(self, entry: Dict[str, Any]) -> str:
        """Extract a unique ID from a feed entry"""
        # Try different ID fields that RSS feeds might use
        return entry.get('id') or entry.get('guid') or entry.get('link') or entry.get('title', '')

    def _create_html_email(self, entry: Dict[str, Any]) -> str:
        """Create HTML email content from feed entry"""
        title = entry.get('title', 'No Title')
        link = entry.get('link', '')
        author = entry.get('author', 'Unknown')
        published = entry.get('published', 'Unknown date')

        # Get content - RSS feeds might have 'content', 'summary', or 'description'
        content = ''
        if 'content' in entry and entry.content:
            content = entry.content[0].value if isinstance(entry.content, list) else entry.content
        elif 'summary' in entry:
            content = entry.summary
        elif 'description' in entry:
            content = entry.description

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    border-bottom: 3px solid #4CAF50;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                h1 {{
                    margin: 0;
                    color: #2c3e50;
                }}
                .meta {{
                    color: #666;
                    font-size: 14px;
                    margin-top: 10px;
                }}
                .content {{
                    margin: 30px 0;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #666;
                    font-size: 14px;
                }}
                a {{
                    color: #4CAF50;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{html.escape(title)}</h1>
                <div class="meta">
                    <strong>Author:</strong> {html.escape(author)} |
                    <strong>Published:</strong> {html.escape(published)}
                </div>
            </div>

            <div class="content">
                {content}
            </div>

            <div class="footer">
                <p><a href="{html.escape(link)}">Read full post on website →</a></p>
                <p style="color: #999; font-size: 12px;">
                    This email was sent by your RSS Monitor. You're receiving this because a new post was detected.
                </p>
            </div>
        </body>
        </html>
        """
        return html_content

    def send_email(self, entry: Dict[str, Any]):
        """Send email notification for a new post"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"New Blog Post: {entry.get('title', 'No Title')}"
            msg['From'] = self.gmail_user
            msg['To'] = self.recipient_email

            # Create HTML content
            html_content = self._create_html_email(entry)

            # Create plain text fallback
            plain_text = f"""
New Blog Post: {entry.get('title', 'No Title')}

Author: {entry.get('author', 'Unknown')}
Published: {entry.get('published', 'Unknown date')}

{entry.get('summary', entry.get('description', 'No description available'))}

Read more: {entry.get('link', '')}
            """.strip()

            # Attach both parts
            part1 = MIMEText(plain_text, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Send email via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.gmail_user, self.gmail_app_password)
                server.send_message(msg)

            print(f"✓ Email sent: {entry.get('title', 'No Title')}")

        except Exception as e:
            print(f"✗ Error sending email: {e}")

    def check_feed(self, is_first_run: bool = False):
        """Check the RSS feed for new posts"""
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking feed...")
            feed = feedparser.parse(self.rss_url)

            if feed.bozo:
                print(f"⚠ Warning: Feed parsing issue - {feed.get('bozo_exception', 'Unknown error')}")

            if not feed.entries:
                print("No entries found in feed")
                return

            if is_first_run:
                print(f"First run detected - marking {len(feed.entries)} existing posts as seen (no emails sent)")
                for entry in feed.entries:
                    post_id = self._get_post_id(entry)
                    self.seen_posts.add(post_id)
                    print(f"  ✓ Marked as seen: {entry.get('title', 'No Title')}")
                self._save_seen_posts()
                print(f"\nSetup complete! Future posts will trigger email notifications.")
                return

            new_posts_count = 0

            # Check each entry
            for entry in feed.entries:
                post_id = self._get_post_id(entry)

                # Skip if already seen
                if post_id in self.seen_posts:
                    continue

                # New post detected - send it!
                print(f"→ New post detected: {entry.get('title', 'No Title')}")
                self.send_email(entry)
                self.seen_posts.add(post_id)
                new_posts_count += 1

            if new_posts_count > 0:
                self._save_seen_posts()
                print(f"✓ Processed {new_posts_count} new post(s)")
            else:
                print("No new posts")

        except Exception as e:
            print(f"✗ Error checking feed: {e}")

    def run(self, interval_minutes: int = 10):
        """
        Run the monitor continuously

        Args:
            interval_minutes: How often to check the feed (default: 10 minutes)
        """
        print("=" * 60)
        print("RSS Feed Monitor Started")
        print("=" * 60)
        print(f"Feed: {self.rss_url}")
        print(f"Sending to: {self.recipient_email}")
        print(f"Check interval: {interval_minutes} minutes")
        print(f"Tracking file: {self.seen_file.absolute()}")
        print("=" * 60)
        print("\nPress Ctrl+C to stop\n")

        # Check if this is the first run (no posts seen yet)
        is_first_run = len(self.seen_posts) == 0

        # Do an initial check
        self.check_feed(is_first_run=is_first_run)

        interval_seconds = interval_minutes * 60

        try:
            while True:
                time.sleep(interval_seconds)
                self.check_feed(is_first_run=False)

        except KeyboardInterrupt:
            print("\n\nMonitor stopped by user")
            print("=" * 60)


def main():
    """Main entry point"""
    # Load configuration from environment variables
    rss_url = os.getenv('RSS_FEED_URL')
    gmail_user = os.getenv('GMAIL_USER')
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', '10'))

    # Validate configuration
    missing = []
    if not rss_url:
        missing.append('RSS_FEED_URL')
    if not gmail_user:
        missing.append('GMAIL_USER')
    if not gmail_app_password:
        missing.append('GMAIL_APP_PASSWORD')
    if not recipient_email:
        missing.append('RECIPIENT_EMAIL')

    if missing:
        print("Error: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        print("\nPlease set these variables or create a .env file")
        print("See .env.example for reference")
        return 1

    # Create and run monitor
    monitor = RSSMonitor(
        rss_url=rss_url,
        gmail_user=gmail_user,
        gmail_app_password=gmail_app_password,
        recipient_email=recipient_email
    )

    monitor.run(interval_minutes=check_interval)
    return 0


if __name__ == '__main__':
    exit(main())
