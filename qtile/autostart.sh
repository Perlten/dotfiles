#!/usr/bin/bash 

picom & # Compositor
nitrogen --restore & # Wallpaper
blueman-applet & # Bluetooth applet
nm-applet & # Network Manager Applet
volumeicon & # PulseAudio applet
xss-lock betterlockscreen -l &  # Lock screen on suspend
pamac-tray & # pacman update applet
dunst & # notification daemon