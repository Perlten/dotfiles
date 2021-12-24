#!/bin/bash

rm -rf ./qtile && echo "removed qtile"
rm -rf ./picom && echo "removed picom"
rm -rf ./autokey && echo "removed autokey"
rm -rf ./rofi && echo "removed rofi"
rm -rf ./dunst && echo "removed dunst"
rm -rf ./bash && echo "removed bash"



cp -r ~/.config/qtile . && echo "Copied qtile configs"
cp -r ~/.config/picom . && echo "Copied picom configs"
cp -r ~/.config/autokey . && echo "Copied autokey configs"
cp -r ~/.config/rofi . && echo "Copied rofi configs"
cp -r ~/.config/dunst . && echo "Copied dunst configs"

mkdir bash && echo "Created bash directory"
cp -r ~/.bashrc ./bash && echo "Copied bashrc configs"
cp -r ~/.shell_aliases ./bash && echo "Copied shell_aliases configs"


