rm -rf instance/
mkdir instance
touch instance/app.db
python manage.py db create_all
flask db init
flask db migrate -m "initial migration"
flask db upgrade