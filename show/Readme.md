### flask server

    python main.py

### redis

    redis-server --daemonize yes

    redis-cli

### Celery Worker and Scheduler together

    Worker - Celery -A celery_tasks.celery worker -l info -B

### Mailhog

    MailHog - navigate to directory "/usr/local/bin" and type "./Mailhog"
