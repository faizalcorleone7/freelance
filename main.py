from fastapi import FastAPI
from dotenv import load_dotenv
from routers import document_router
import uvicorn

load_dotenv()

app = FastAPI(title="Document Vector Search Service")
app.include_router(document_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
