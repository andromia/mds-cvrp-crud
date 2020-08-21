rm -rf instance/
mkdir instance
touch instance/app.db
python manage.py db create_all