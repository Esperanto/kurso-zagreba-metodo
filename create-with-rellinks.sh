#!/bin/bash
# Ĉi tiu skripto kreas ĉiujn paĝojn kaj reskribas ilin tiel ke ili povu esti uzataj en ekzemple
# Github Pages kaj ipfs sen aldonaj ŝanĝoj. La celo de ĉi tio estas faciligi testadon de postaj
# ŝanĝoj, kiel ekzemple la implementado de la PWA-dosieroj.
git stash
git reset --hard
git stash apply
python generate.py
export baselink=$1
for file in `find html/output/ -name \*.html`; do sed -i -r "s@src=\"/@src=\"$baselink@g" $file ; done 
for file in `find html/output/ -name \*.html`; do sed -i -r "s@href=\"/@href=\"$baselink@g" $file ; done 
