from celery import Celery

celery = Celery(
    'blog_tasks', 
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery.conf.update(
    imports=["consumer_tasks"]
)
