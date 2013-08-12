#This runs the management command that generated a static HTML page of the whole regulation. 
#It does this for the latest Regulation E. 

pip install -q -r requirements.txt
pip install -q -r requirements-test.txt
python manage.py generate_regulation --regulation=1005 --reg_version=2013-10604-eregs --settings=regserver.settings.dev --traceback
