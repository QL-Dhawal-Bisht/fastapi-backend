import os
import sys


from fastapi import FastAPI
from dotenv import load_dotenv
from configs.database import engine, Base
from routes.api import router as api_router

load_dotenv()

app = FastAPI()

# CReate database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(api_router, prefix="")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
