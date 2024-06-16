from celery import Celery, Task

def create_celery(app):
    celery = Celery(
        app.import_name,
        backend = app.config['RESULT_BACKEND'],
        broker = app.config['BROKER_URL'],
        timezone = app.config['TIME_ZONE']
    )
    celery.conf.update(app.config)
    # celery.conf.timezone = 'Asia/Kolkata'
    # TaskBase = celery.Task
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                print("Starting a new task")
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery