#!/bin/bash
# RSS Monitor Auto-Start Setup Script

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_NAME="com.rssmonitor.plist"
PLIST_SOURCE="$SCRIPT_DIR/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "RSS Monitor Auto-Start Setup"
echo "=============================="
echo ""

case "$1" in
    install)
        echo "Installing RSS Monitor to start automatically..."

        # Create LaunchAgents directory if it doesn't exist
        mkdir -p "$HOME/Library/LaunchAgents"

        # Copy the plist file
        cp "$PLIST_SOURCE" "$PLIST_DEST"
        echo "✓ Copied configuration to ~/Library/LaunchAgents/"

        # Load the service
        launchctl load "$PLIST_DEST"
        echo "✓ Service loaded and started"

        echo ""
        echo "RSS Monitor is now running in the background!"
        echo "It will automatically start when you log in."
        echo ""
        echo "To check status: ./setup_autostart.sh status"
        echo "To view logs:    ./setup_autostart.sh logs"
        ;;

    uninstall)
        echo "Uninstalling RSS Monitor auto-start..."

        # Unload the service
        launchctl unload "$PLIST_DEST" 2>/dev/null
        echo "✓ Service stopped"

        # Remove the plist file
        rm -f "$PLIST_DEST"
        echo "✓ Configuration removed"

        echo ""
        echo "RSS Monitor auto-start has been removed."
        echo "You can still run it manually with: python rss_monitor.py"
        ;;

    restart)
        echo "Restarting RSS Monitor..."
        launchctl unload "$PLIST_DEST" 2>/dev/null
        launchctl load "$PLIST_DEST"
        echo "✓ Service restarted"
        ;;

    status)
        echo "Checking RSS Monitor status..."
        echo ""

        if launchctl list | grep -q "com.rssmonitor"; then
            echo "✓ RSS Monitor is running"
            echo ""
            echo "Recent log entries:"
            tail -n 10 "$SCRIPT_DIR/rss_monitor.log" 2>/dev/null || echo "No logs yet"
        else
            echo "✗ RSS Monitor is not running"
            echo ""
            echo "To start it: ./setup_autostart.sh install"
        fi
        ;;

    logs)
        echo "RSS Monitor Logs (press Ctrl+C to stop)"
        echo "========================================"
        tail -f "$SCRIPT_DIR/rss_monitor.log"
        ;;

    *)
        echo "RSS Monitor Auto-Start Management"
        echo ""
        echo "Usage: $0 {install|uninstall|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  install   - Install and start RSS Monitor to run automatically"
        echo "  uninstall - Stop and remove auto-start"
        echo "  restart   - Restart the RSS Monitor service"
        echo "  status    - Check if RSS Monitor is running"
        echo "  logs      - View live logs"
        echo ""
        exit 1
        ;;
esac

exit 0
