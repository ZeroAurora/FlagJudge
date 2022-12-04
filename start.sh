flask --app flagjudge initdb
flask --app flagjudge preload
gunicorn -w 4 -b 0.0.0.0 flagjudge:app
