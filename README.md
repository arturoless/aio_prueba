0.- Create database and tables (use PostgreSQL)
1.- Create env:
    py -m venv env
2.- Activate env (Windows) :
    env\Scripts\activate
3.- Install libraries:
    pip install -r requirements.txt
    
6.- Run server:
    py server.py

6.- In other terminal with the same env, Run client:
    py client.py

7.- In an additional terminal, set the same environment and run celery: 
    celery -A main.celery worker --loglevel=info --pool=solo


Postman Collection: https://www.getpostman.com/collections/3adddd220bb5bda54177