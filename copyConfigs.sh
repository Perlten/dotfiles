#!/bin/bash

git pull

rm -r ~/.config/qtile && cp -r ./qtile ~/.config && echo "Copied qtile configs"
rm -r ~/.config/picom && cp -r ./picom ~/.config && echo "Copied picom configs"
rm -r ~/.config/autokey && cp -r ./autokey ~/.config && echo "Copied autokey configs"
rm -r ~/.config/rofi && cp -r ./rofi ~/.config && echo "Copied rofi configs"
rm -r ~/.config/dunst && cp -r ./dunst ~/.config && echo "Copied dunst configs"

cp ./bash/.bashrc ~/.bashrc && echo "Copied bashrc configs"
cp ./bash/.shell_aliases ~/.shell_aliases && echo "Copied shell_aliases configs"
