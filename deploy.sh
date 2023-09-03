python -a venv env
source env/bin/activate
pip3 install -r requirments.txt
python3 manage.py migrate
deactivate