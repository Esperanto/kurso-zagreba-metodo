git push

# Create pages for
# http://esperanto.github.io/kurso-zagreba-metodo/html/output/
git checkout gh-pages
git merge master -m "Merge from master."
python generate.py /kurso-zagreba-metodo/html/output/
git add -f html/output/*
git commit -m "Updated output for gh-pages."
git push origin gh-pages
git checkout master

# Create pages for
# http://learn.esperanto.com/
git checkout root-pages
git merge master -m "Merge from master."
python generate.py /
git add -f html/output/*
git commit -m "Updated output for root-pages."
git push origin root-pages
git checkout master
