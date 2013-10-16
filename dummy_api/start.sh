#!/bin/bash
git clone https://github.com/eregs/regulations-core.git
cd regulations-core
pip install zc.buildout
buildout

./bin/django syncdb
./bin/django migrate
./bin/django runserver 8282 &
sleep 5 # give django enough time to startup

# Load the data
cd ../dummy_api
for TAIL in $(find */* -type f | sort -r)
do
    curl -X PUT http://localhost:8282/$TAIL -d @$TAIL
done
