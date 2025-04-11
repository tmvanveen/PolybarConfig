#!/bin/bash
# scrollNieuws.sh
NEWS_SCRIPT="$HOME/.config/polybar/nieuws.sh"

# Infinite loop
while true; do
    # Get news items one by one
    mapfile -t NEWS_ITEMS < <($NEWS_SCRIPT)
    
    # Process each news item separately
    for ITEM in "${NEWS_ITEMS[@]}"; do
        TEXT_LENGTH=${#ITEM}
        WINDOW=150
        
        # Scroll this individual item
        for ((i = 0; i <= TEXT_LENGTH - WINDOW; i++)); do
            DISPLAY_TEXT="${ITEM:$i:$WINDOW}"
            echo "$DISPLAY_TEXT"
            sleep 0.3
        done
        
        # Show the beginning again briefly
        echo "${ITEM:0:$WINDOW}"
        sleep 5  # Pause between news items
    done
done
