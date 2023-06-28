# Liberty Test Task

##The task:

Create a REST API that returns the combined posts and comments provided from 
these two endpoints, while caching the responses:

https://jsonplaceholder.typicode.com/posts

https://jsonplaceholder.typicode.com/comments

 
## Local Setup

**Make a copy from ".env.example" with name ".env" in the same folder.**
This file will contain default settings for the project setup.

GET_POSTS_URL and GET_COMMENTS_URI are URI's of GET endpoints to fetch data from. 
Set DEBUG to True if you want to see logs of SQL Queries - 
let's say for the sake of checking caching functionalty

Run to start container:
```
docker-compose up
```

## API description:

1. **GET localhost:8000/refetch_posts_and_comments** - fetches posts and comments from endpoints specified in .env (.env.example) file. It also cleans the Redis cache. Use this endpoint after the app started to fulfill database with data needed. 
2. **GET localhost:8000/posts** - returns all the posts with relevant comments. This endpoint responses are getting cached.
3. **GET localhost:8000/posts/<id>** - returns post instance with id passed in. This endpoint responses are getting cached.

And there are also several additional endpoints - they are not required by the initial task:
4. GET localhost:8000/comments - returns all the comments. This endpoint responses are not getting cached.
5. GET localhost:8000/comments/<id> - returns comment instance with id passed in. This endpoint responses are not getting cached.

## Running tests

Run to start container:
```
docker-compose up
```
Wait until the services in container properly started and then run tests:
```
docker-compose run liberty_test_task_api pytest
```
