Documentation (Readme) -

Prerequisites ->
Python 3.9+
Redis with Redisearch module

Installation ->

1. Clone the repository
2. Create and activate a virtual environment
3. Install the dependencies (pip install -r requirements.txt)
4. Set up Redis with Redisearch
5. Set environment variables:
   export REDIS_HOST=localhost
   export REDIS_PORT=6379
6. Run the FastAPI application (uvicorn main:app --reload)

I used the Redisearch module to enable full-text search and vector similarity search capabilities in Redis.
Performance enhancing decision(s) -> Thread Pool Executor: I used a thread pool executor to handle document processing in parallel, improving the performance of the upload endpoint.
