from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from consumer_tasks import create_blog_task, delete_blog_task, update_blog_task

es_endpoint = "https://5aee913c276a43a99f410aaa729119e0.us-central1.gcp.cloud.es.io"
es_api_key = "NHF0NzA1RUI1XzUtT0lkSkp4V0s6S2gwakFWcVBROVdTQklaZ1BxaTFCZw=="
es_client = Elasticsearch(es_endpoint, api_key=es_api_key)

app = FastAPI()
class Blog_Structure(BaseModel):
    title: str
    body: str
    user_id: str

@app.post("/blog")
async def create_blog(blog: Blog_Structure):
    try:
        blog_doc = blog.dict()
        create_blog_task.delay(blog_doc)
        return {"message": "Recieved the blog. Gr8 Job!!!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting blog: {str(e)}")
        
@app.get("/blog_search")
async def blog_search(query_string: str):
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match_phrase": {
                            "title": query_string
                        }
                    },
                    {
                        "match_phrase": {
                            "body": query_string
                        }
                    }
                ]
            }
        }
    }
    response = es_client.search(index="blog_data", body=query)
    return response['hits']['hits']

@app.get("/blog_search/{user_id}")
async def blog_search_by_user(user_id: str):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "user_id": user_id
                        }
                    }
                ]
            }
        }
    }
    response = es_client.search(index="blog_data", body=query)
    return response['hits']['hits']

@app.put("/blog/{blog_id}")
async def update_blog(blog_id: str, blog: Blog_Structure):
    try:
        blog_doc = blog.dict()
        update_blog_task.delay(blog_id, blog_doc)

        return {"message": "Great edit: Blog updated!!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating blog: {str(e)}")

@app.delete("/blog/{blog_id}")
async def delete_blog(blog_id: str):
     try:
        delete_blog_task.delay(blog_id)
        print(es_client.delete(index="blog_data", id=blog_id))
        return {"message": "I am sure you had your reasons.Blog deleted!!!"}
     except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error queuing blog deletion: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8800, reload=True, debug=True)