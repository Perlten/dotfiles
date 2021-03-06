#!/bin/bash


die () {
    echo >&2 "$@"
    exit 1
}

rm -rf ./picom && echo "removed picom"
rm -rf ./autokey && echo "removed autokey"
rm -rf ./rofi && echo "removed rofi"
rm -rf ./dunst && echo "removed dunst"
rm -rf ./bash && echo "removed bash"

cp -r ~/.config/picom . && echo "Copied picom configs"
cp -r ~/.config/autokey . && echo "Copied autokey configs"
cp -r ~/.config/rofi . && echo "Copied rofi configs"
cp -r ~/.config/dunst . && echo "Copied dunst configs"

mkdir bash && echo "Created bash directory"
cp -r ~/.bashrc ./bash && echo "Copied bashrc configs"
cp -r ~/.shell_aliases ./bash && echo "Copied shell_aliases configs"

git status
[ "$#" -eq 1 ] || die "1 argument required, $# provided"
git add --all && \
git commit -m "$1" && \
git push
