git log --format="    - nomo: %aNXXX      retpoŝto: %aeXXX      github: %aN" enhavo/tradukenda/$1 | sort | uniq |sed  's/XXX/\'$'\n/g' | mvim -
