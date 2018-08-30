#!/bin/bash
# Ĉi tiu skripto kreas ĉiujn paĝojn kaj eventuale reskribas ilin por Github Pages.
# Sekve al tio ĝi preparas la paĝojn por ke ili funkciu kiel Progressive Web App.
# Alvoku kiel ./prepare-pwa.sh https://esperanto.github.io/kurso-zagreba-metodo/
git stash
git reset --hard
git stash apply
python generate.py
export baselink=$1
for file in `find html/output/ -name \*.html`; do sed -i -r "s@src=\"/@src=\"$baselink@g" $file ; done 
for file in `find html/output/ -name \*.html`; do sed -i -r "s@href=\"/@href=\"$baselink@g" $file ; done 
cp -r projects/PWA/Images html/output/images
cp -r projects/PWA/manifest.json html/output/manifest.json
sed -i 's@https://learn.esperanto.com/@$baselink@' html/output/manifest.json
sed -i 's@/images@images@' html/output/manifest.json
(cd html/output/ ; wget https://raw.githubusercontent.com/boyofgreen/ManUp.js/master/manup.js)
cp projects/serviceWorker2/* html/output/
sed -i '/<\/body>/i \
	<script src="manup.js"></script>\
	<script src="pwabuilder-sw-register.js"></script>' html/output/index.html
