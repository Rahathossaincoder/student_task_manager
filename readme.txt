-------at end ------pip freeze > requirements.txt

1. Start with python virtual box:
-----------------------------------------------------------------------------------------------
python3 -m venv venv

source venv/bin/activate

-----------------------------------------------------------------------------------------------

2.  pip install django
    django-admin startproject student_task_manager .

-----------------------------------------------------------------------------------------------

3.  python manage.py startapp tasks
    python manage.py startapp users

-----------------------------------------------------------------------------------------------

4.  python manage.py makemigrations
    python manage.py migrate

-----------------------------------------------------------------------------------------------

