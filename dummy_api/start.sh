#!/bin/bash
git clone https://github.com/cfpb/regulations-core.git
cd regulations-core
pip install -r requirements.txt

python manage.py syncdb
python manage.py migrate
python manage.py runserver 8282 &
sleep 5 # give django enough time to startup

# Load the data
cd ../dummy_api
for TAIL in $(find */* -type f | sort -r)
do
    curl -X PUT http://localhost:8282/$TAIL -d @$TAIL
done
