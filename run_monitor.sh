#!/bin/bash
# RSS Feed Monitor Runner
# This script makes it easy to run the monitor in the background

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

case "$1" in
    start)
        echo "Starting RSS Monitor..."
        if [ -f .env ]; then
            echo "Using configuration from .env file"
        else
            echo "Warning: .env file not found. Make sure environment variables are set."
        fi
        nohup python3 rss_monitor.py > rss_monitor.log 2>&1 &
        echo "Monitor started in background (PID: $!)"
        echo "Check logs with: tail -f rss_monitor.log"
        ;;

    stop)
        echo "Stopping RSS Monitor..."
        pkill -f rss_monitor.py
        echo "Monitor stopped"
        ;;

    status)
        if pgrep -f rss_monitor.py > /dev/null; then
            echo "RSS Monitor is running"
            ps aux | grep rss_monitor.py | grep -v grep
        else
            echo "RSS Monitor is not running"
        fi
        ;;

    logs)
        if [ -f rss_monitor.log ]; then
            tail -f rss_monitor.log
        else
            echo "No log file found"
        fi
        ;;

    restart)
        $0 stop
        sleep 2
        $0 start
        ;;

    *)
        echo "RSS Feed Monitor Control Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the monitor in the background"
        echo "  stop    - Stop the monitor"
        echo "  restart - Restart the monitor"
        echo "  status  - Check if monitor is running"
        echo "  logs    - Show monitor logs (Ctrl+C to exit)"
        exit 1
        ;;
esac

exit 0
