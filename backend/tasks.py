from backend import celery

@celery.task()
def my_background_task():
    print('123')
    return 'working'