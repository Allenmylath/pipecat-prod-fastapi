import asyncio
import uvicorn
import os
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from bot import main

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        print("New WebSocket connection request")
        await websocket.accept()
        print("WebSocket connection accepted")
        
        # Call main with the websocket parameter
        await main(websocket)
        
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")

if __name__ == "__main__":
    # Get port from environment variable for Heroku compatibility
    port = int(os.getenv("PORT", 8765))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
