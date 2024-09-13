from elasticsearch import Elasticsearch
from celery_app import celery

es_client = Elasticsearch("https://5aee913c276a43a99f410aaa729119e0.us-central1.gcp.cloud.es.io", 
                          api_key="NHF0NzA1RUI1XzUtT0lkSkp4V0s6S2gwakFWcVBROVdTQklaZ1BxaTFCZw==")

@celery.task
def create_blog_task(blog_doc):
    try:
        es_client.index(index="blog_data", document=blog_doc)
        print(f"Blog created: {blog_doc}")
    except Exception as e:
        print(f"Error creating blog: {e}")

@celery.task
def delete_blog_task(blog_id):
    try:
        es_client.delete(index="blog_data", id=blog_id)
        print(f"Blog deleted with id: {blog_id}")
    except Exception as e:
        print(f"Error deleting blog: {e}")

@celery.task
def update_blog_task(blog_id, blog_doc):
    try:
        es_client.index(index="blog_data", document=blog_doc, id=blog_id)
        print(f"Blog updated with id: {blog_id}")
    except Exception as e:
        print(f"Error updating blog: {e}")
