git push

# Hereda skripto por la malnova root-pages-fluo.
# La aktuala prova deplojo uzas GitHub Pages el eligo/retejo.
git checkout root-pages
git merge master -m "Merge from master."
make html-all
git add -f eligo/retejo/*
git commit -m "Updated output for root-pages."
git push origin root-pages
git checkout master
