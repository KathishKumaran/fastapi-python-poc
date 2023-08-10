# # main.py
import asyncio
import uvicorn
from fastapi import FastAPI
from auth.routes import auth_router
from models.models import Base
from database import engine
from logger import logger  # Import the logger

app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
def shutdown():
    engine.dispose()
    logger.info("Application shutting down")

async def main():
    host = "127.0.0.1"
    port = 3000
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)

    logger.info(f"Server listening at http://{host}:{port}")  # Log the server startup message
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
