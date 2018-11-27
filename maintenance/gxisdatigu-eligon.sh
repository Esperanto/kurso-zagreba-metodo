# Move to main dir.
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH/..

LAST_SAFE_COMMIT=`cat maintenance/last-safe-commit.txt`

git pull -q
git checkout $LAST_SAFE_COMMIT generate.py
git checkout $LAST_SAFE_COMMIT html/main.py
git checkout $LAST_SAFE_COMMIT html/output/index.html

# Check if anything new.
LAST_COMMIT=`git rev-parse HEAD`
LAST_GENERATED_COMMIT=`cat maintenance/last-generated-commit.txt`

# If nothing new: exit.
if [ $LAST_COMMIT = $LAST_GENERATED_COMMIT ]
then
	exit 
fi

for l in ar ca cs de en es fa fr frp he hr hu id it kk km ko lo ms my nl pl pt ru sk sl sv th tr uk ur vi zh zh-tw
do
	python2 generate.py -l $l
done

git rev-parse HEAD > maintenance/last-generated-commit.txt
