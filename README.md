Library Management System -MAD2
Technologies Used
Flask
Vue3
Redis
Celery
SQLite
Installation
Please run the following commands on the terminal.

.venv/Scripts/Activate.ps1 or source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt
Once the setup is done, use the following script in the terminal to activate the virtual environment-

.venv/Scripts/Activate.ps1 or source .venv/bin/activate

Then use the following script in the terminal to run the code-

python upload_initial_data.py
Use the following script to deactivate the virtual environment-

deactivate

To run the redis, celery and mailhog services-

celery -A main:celery_app worker --loglevel INFO
celery -A main:celery_app beat --loglevel INFO
go/bin/MailHog
In case of any problem in running the redis server, run the following commands-

sudo service redis-server stop
To install all the vue dependencies for the frontend-

npm install

To start the frontend-

npm run serve
