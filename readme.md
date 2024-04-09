#create an environment
python -m venv env (if not works , try python3 -m venv env)

#Install requirements
pip install -r requirements.txt

#Makemigrations for first time
python manage.py migrate

#Runserver
python manage.py runserver



