setup:
	#rm db.sqlite
	python manage.py migrate
	python manage.py loaddata testdata
migrate:
	python manage.py makemigrations
	python manage.py migrate
