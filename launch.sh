#!/usr/bin/env bash

# Terminate already running bar instances
killall -q polybar

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

# Launch bars on both monitors
polybar --reload myconf -c ~/.config/polybar/config.ini &
polybar --reload myconf -c ~/.config/polybar/config-right.ini &

echo "Polybar launched..."
