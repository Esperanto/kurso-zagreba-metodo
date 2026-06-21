# Move to main dir.
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH/..

LAST_SAFE_COMMIT=`cat iloj/last-safe-commit.txt`

git pull -q
git checkout $LAST_SAFE_COMMIT fonto/py/generu.py 2> /dev/null
git checkout $LAST_SAFE_COMMIT fonto/py/html.py 2> /dev/null
git checkout $LAST_SAFE_COMMIT fonto/html/radiko.html 2> /dev/null

# Check if anything new.
LAST_COMMIT=`git rev-parse HEAD`
LAST_GENERATED_COMMIT=`cat iloj/last-generated-commit.txt`

# If nothing new: exit.
if [ $LAST_COMMIT = $LAST_GENERATED_COMMIT ]
then
	exit 
fi

# for l in ar ca cs da de el en es fa fr frp ga he hi hr hu id it ja kk km ko ku lo mg ms my nl pl pt ro ru sk sl sv sw th tok tr uk ur vi yo zh zh-tw
#for l in ar ca cs da de el en es fa fr frp ga he hi hr hu id it ja kk km ko ku lo mg ms my nl pl pt ro ru sk sl sv sw th tr uk ur vi yo zh zh-tw
for l in ar ca cs da de el en es fa fr frp ga he hi hr hu id it ja kk km ko lo mg ms my nl pl pt ro ru sk sl sv sw th tr uk ur vi yo zh zh-tw
do
	/home/stc/leo/.venv/bin/python -m fonto.py.generu -l $l
done

git rev-parse HEAD > iloj/last-generated-commit.txt
