release: python short_text_api/manage.py makemigrations
release: python short_text_api/manage.py makemigrations api
release: python short_text_api/manage.py migrate
web: python short_text_api/manage.py runserver 0.0.0.0:$PORT --noreload
web: gunicorn short_text_api.wsgi --log-file
