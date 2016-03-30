git checkout gh-pages
git merge master -m "Merge from master."
python generate.py /kurso-zagreba-metodo/html/output/
git add -f html/output/*
git commit -m "Updated output for gh-pages."
git push origin gh-pages
git checkout master
