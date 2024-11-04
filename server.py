import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

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
        
        # Create a global websocket_client variable that bot.py can access
        global websocket_client
        websocket_client = websocket
        
        # Import and run the bot
        from bot import main
        await main()
        
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8765,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
