#!/bin/bash
# Ĉi tiu skripto kreas ĉiujn paĝojn kaj eventuale reskribas ilin por Github Pages.
# Sekve al tio ĝi preparas la paĝojn por ke ili funkciu kiel Progressive Web App.
# Alvoku kiel ./fonto/pwa/prepare-pwa.sh https://esperanto.github.io/kurso-zagreba-metodo/
git stash
git reset --hard
git stash apply
export baselink=$1
[ "x$baselink" == "x" ] && export baselink="https://esperanto.github.io/kurso-zagreba-metodo/" && echo "No baselink given as parameter, using $baselink"
make html-all
for file in `find eligo/retejo/ -name \*.html`; do sed -i -r "s@src=\"/@src=\"$baselink@g" $file ; done
for file in `find eligo/retejo/ -name \*.html`; do sed -i -r "s@href=\"/@href=\"$baselink@g" $file ; done
cp -r fonto/pwa/Images eligo/retejo/images
cp -r fonto/pwa/manifest.json eligo/retejo/manifest.json
sed -i "s@https://esperanto12.net/@$baselink@" eligo/retejo/manifest.json
sed -i 's@/images@images@' eligo/retejo/manifest.json
(cd eligo/retejo/ ; wget https://raw.githubusercontent.com/boyofgreen/ManUp.js/master/manup.js)
cp fonto/pwa/pwabuilder-sw* eligo/retejo/
sed -i '/<\/body>/i \
	<script src="manup.js"></script>\
	<script src="pwabuilder-sw-register.js"></script>' eligo/retejo/index.html
sed -i '/<title>/i \
	<link rel="manifest" href="manifest.json">' eligo/retejo/index.html
