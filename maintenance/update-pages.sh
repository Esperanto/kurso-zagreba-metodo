git add html/output
git commit -am "Updated output"
git push
git checkout gh-pages
git merge master -m "Merge from master."
git push origin gh-pages
git checkout master
