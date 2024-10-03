# Library Management System - MAD2

A multi-user library management system built with Flask, Vue3, Redis, Celery, and SQLite.

## Technologies Used
- Flask
- Vue3
- Redis
- Celery
- SQLite

## Installation

## Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   
2. Set up and activate the virtual environment:

- On Windows:
```bash
.venv/Scripts/Activate.ps1
```
- On Linux/MacOS:
```bash
source .venv/bin/activate
```
3. Upgrade pip:
```bash
pip install --upgrade pip
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Backend

1. Activate the virtual environment (if not already active):

- On Windows:
```bash
.venv/Scripts/Activate.ps1
```
- On Linux/MacOS:
```bash
source .venv/bin/activate
```

### Running Redis, Celery, and Mailhog Services

1. Run the Celery worker:
```bash
celery -A main:celery_app worker --loglevel INFO
```

2. Run the Celery beat scheduler:
```bash
celery -A main:celery_app beat --loglevel INFO
```

3. Run MailHog (for testing email sending):
```bash
go/bin/MailHog
```

### In Case of Redis Server Issues

1. If there are problems running the Redis server, stop it first:
```bash
sudo service redis-server stop
```

## Frontend Setup

1. Install all Vue dependencies:
```bash
npm install
```

2. Start the frontend:
```bash
npm run serve
```
