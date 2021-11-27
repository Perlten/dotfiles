#!/usr/bin/env bash 

picom &
nitrogen --restore &
blueman-applet &
nm-applet &
pa-applet &
xss-lock betterlockscreen -l & 
pamac-tray &
dunst &