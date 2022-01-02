#!/bin/bash

cp -r ./qtile ~/.config && echo "Copied qtile configs"
cp -r ./picom ~/.config && echo "Copied picom configs"
cp -r ./autokey ~/.config && echo "Copied autokey configs"
cp -r ./rofi ~/.config && echo "Copied rofi configs"
cp -r ./dunst ~/.config && echo "Copied dunst configs"

cp ./bash/.bashrc ~/.bashrc && echo "Copied bashrc configs"
cp ./bash/.shell_aliases ~/.shell_aliases && echo "Copied shell_aliases configs"