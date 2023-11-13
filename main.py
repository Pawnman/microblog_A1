from fastapi import FastAPI
from pymongo import MongoClient
import uvicorn
from router import router,get_collection
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)