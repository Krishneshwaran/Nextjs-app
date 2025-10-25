from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from contextlib import asynccontextmanager

# Global variable to cache the status
status_cache = {"is_active": False}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    task = asyncio.create_task(fetch_status_periodically())
    yield
    # Shutdown
    task.cancel()

async def fetch_status_periodically():
    client = AsyncIOMotorClient("mongodb+srv://krish:krish@study.po9dv.mongodb.net/")
    db = client.venom
    collection = db.state
    while True:
        try:
            doc = await collection.find_one()
            if doc:
                status_cache["is_active"] = doc["is_active"]
                print(f"Fetched status: {status_cache['is_active']}")
            else:
                print("No document found")
        except Exception as e:
            print(f"Error fetching status: {e}")
        await asyncio.sleep(2)  # 2 seconds

app = FastAPI(lifespan=lifespan)

@app.get("/status")
async def get_status():
    return status_cache