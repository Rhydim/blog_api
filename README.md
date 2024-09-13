# BLOG API

# FastAPI, Celery, Redis, and Elasticsearch Application

This project is a blog application built with FastAPI for the backend, Celery for asynchronous task processing, Redis as a message broker, and Elasticsearch for indexing and searching blogs. The application can be run locally, using Docker, or deployed to a Kubernetes cluster.

## Table of Contents
1. [Project Setup](#project-setup)
2. [Running Locally](#running-locally)
3. [Running with Docker](#running-with-docker)
5. [Example Curls](#example-curls)

## Project Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Kubernetes (GKE, EKS, AKS or other providers)
- Redis and Elasticsearch should be available if running locally

### Install Dependencies

 1. Clone the repository:
    ```bash
    git clone https://github.com/Rhydim/blog_api.git
    cd blog-api
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
4. Start Redis, FastAPI, and Celery:
    ```bash
    redis-server
    uvicorn main:app --reload --port 8800
    celery -A celery_app.celery worker --loglevel=info
# Running with Docker
1. Build and start the services:
    ```bash
    docker-compose up --build
2. To stop the services:
    ```bash
    docker-compose down
# Example Curls
1. Create a new blog (POST Request)
    ```bash
    curl -X 'POST' \
    'http://0.0.0.0:8800/blog' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "title": "Curl Eg 001",
    "body": "Lorem Ipsum dolar lit",
    "user_id": "John Doe"
    }'
2. Search blog with title or body (GET Request)
    ```bash
    curl -X 'GET' \
   'http://0.0.0.0:8800/blog_search?query_string=Curl Eg' \
   -H 'accept: application/json'
3. Search blog with user id:
    ```bash
    curl -X 'GET' \
    'http://0.0.0.0:8800/blog_search?query_string=Kubernetes' \
    -H 'accept: application/json'
4. Update Existing blog using document id(PUT Request)
    ```bash
    curl -X 'PUT' \
    'http://0.0.0.0:8800/blog/A_cZ6pEBDVhtpB5hm-Nc' \
    -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{
      "title": "Curl Update Eg 001",
      "body": "Lorem Ipsum Update",
          "user_id": "John Doe"
        }'
5. Delete existing blog using doc id (DELETE Request)
    ```bash
    curl -X 'DELETE' \
    'http://0.0.0.0:8800/blog/A_cZ6pEBDVhtpB5hm-Nc' \
    -H 'accept: application/json'
