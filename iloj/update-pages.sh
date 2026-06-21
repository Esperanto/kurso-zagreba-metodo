git push

# Create pages for
# http://esperanto12.net/
git checkout root-pages
git merge master -m "Merge from master."
python generate.py /
git add -f html/output/*
git commit -m "Updated output for root-pages."
git push origin root-pages
git checkout master
