# NeRFCFM API
Backend for the NerFCFM project.

## Important
This is a basic implementation for the NerFCFM API, it does not consider many security settings. Use this only for testing.

### Dependecies
- Django (REST Backend)
- Celery (Task Queue)
- Redis (Message Broker)

### Instructions
 On a Linux Machine

 1. Make sure to [install Nerfstudio using conda](https://docs.nerf.studio/quickstart/installation.html)

 2. Clone this repository

 3. Django setup
    ```bash
    # virtual environment setup
    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # migrations
    python manage.py makemigrations api
    python manage.py migrate

    # load initial data
    python manage.py load_nerfs
    python manage.py load_data_types
    ```

4. Redis Broker (use screen or new terminal)
    ```bash
    # Arch
    sudo pacman -S redis
    # Debian / Ubuntu
    sudo apt-get install redis

    # start redis server
    redis-server
    ```

5. Start Celery (use screen or new terminal)
    ```bash
    celery -A nerfcfm.celery worker --loglevel=info
    ``` 

6. Create `.env` file at root directory
    ```bash
    # if you want to test with nerf studio, set this to False
    USE_TEST_SCRIPT = True
    # test script will use a random value between these two
    MAX_TIME_SCRIPT = 100
    MIN_TIME_SCRIPT = 10
    ```

6. Run the API
    ```bash
    python manage.py runserver 8000
    ```
