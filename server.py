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

async def heartbeat(websocket: WebSocket):
    """Send ping message every 30 seconds to keep connection alive"""
    try:
        while True:
            await asyncio.sleep(30)
            await websocket.send_text("ping")
            print("Ping sent")
    except Exception as e:
        print(f"Heartbeat error: {e}")
        raise

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        print("New WebSocket connection request")
        await websocket.accept()
        print("WebSocket connection accepted")
        
        # Start heartbeat task
        heartbeat_task = asyncio.create_task(heartbeat(websocket))
        
        try:
            # Call main with the websocket parameter
            await main(websocket)
        finally:
            # Cancel heartbeat when main exits
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass
            
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
