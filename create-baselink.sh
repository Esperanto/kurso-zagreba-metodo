#!/bin/bash
# Ĉi tiu skripto kreas ĉiujn paĝojn kaj eventuale reskribas ilin por Github Pages.
# Alvoku kiel ./create-baselink.sh https://esperanto.github.io/kurso-zagreba-metodo/
git stash
git reset --hard
git stash apply
python generate.py
export baselink=$1
for file in `find html/output/ -name \*.html`; do sed -i -r "s@src=\"/@src=\"$baselink@g" $file ; done 
for file in `find html/output/ -name \*.html`; do sed -i -r "s@href=\"/@href=\"$baselink@g" $file ; done 
