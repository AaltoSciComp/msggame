test:
	python manage.py test
setup:
#	rm db.sqlite3
	python manage.py migrate
	python manage.py loaddata testdata
migrate:
	python manage.py makemigrations
	python manage.py migrate
