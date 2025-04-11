This is my current polybar config and all the modules that are associated with it

Change the permissions of all the files; sudo chmod +x *

Use launch.sh to start the Polybar including config, in i3 it is;

# Status Bar (polybar)
exec_always --no-startup-id ./.config/polybar/launch.sh
