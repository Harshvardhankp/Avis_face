python watchf_multithread.py &
python application.py &

gunicorn --bind 0.0.0.0:5000 wsgi
gunicorn --bind 0.0.0.0:5000 wsgi
