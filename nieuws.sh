#!/bin/bash
# nieuws.sh
RSS_URLS=(
    "FD|https://fd.nl/?rss"
    "NU|https://www.nu.nl/rss"
    "GS|https://www.geenstijl.nl/feeds/recent.atom"
)

# Loop through each RSS URL and get titles
for ENTRY in "${RSS_URLS[@]}"; do
    PREFIX=$(echo "$ENTRY" | cut -d'|' -f1)
    URL=$(echo "$ENTRY" | cut -d'|' -f2)
    
    # Fetch the feed
    FEED=$(curl -s --connect-timeout 5 "$URL")
    
    # Check if it's an Atom feed (contains <entry>) or RSS feed (contains <item>)
    if echo "$FEED" | grep -q "<entry>"; then
        # Atom feed parsing
        echo "$FEED" | xmlstarlet sel -N atom="http://www.w3.org/2005/Atom" -t -v "//atom:entry/atom:title" -n 2>/dev/null | \
            grep . | \
            head -n 3 | \
            sed "s/^/[$PREFIX] /"
    else
        # RSS feed parsing
        echo "$FEED" | xmlstarlet sel -t -v "//item/title" -n 2>/dev/null | \
            grep . | \
            head -n 3 | \
            sed "s/^/[$PREFIX] /"
    fi
done
