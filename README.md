# nerfcfm-back
Backend for the NerFCFM project.

## Important
This is basic implementation for the NerFCFM backend, it does not consider many security settings. Use this only for testing.

 ### Instructions
 On a Linux Machine

 1. Make sure to install Nerfstudio using conda
 2. Clone this repository
 3. Project Setup
```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py load_nerfs
python manage.py load_data_types
```
4. Redis Broker (use screen or other terminal)
```bash
# Arch
sudo pacman -S redis
# Debian / Ubuntu
sudo apt get redis

# start redis server
redis-server
```

5. Start Celery (use screen or other terminal)
```bash
celery -A nerfcfm.celery worker --loglevel=info
``` 

6. Create env file (example)
```bash
# if you want to test without nerfstudio
USE_TEST_SCRIPT = True
MAX_TIME_SCRIPT = 100
MIN_TIME_SCRIPT = 10
```

6. Run the API
```bash
python manage.py runserver 8000
```
