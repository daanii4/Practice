from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.database import Base, engine
from app.routes import (
    auth_routes,
    facebook_auth,
    ad_generation_routes,
    ad_performance_routes,
    media_assets,
    projects,
    users
)
from app.auth import auth_base_router  # Importing from auth.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.responses import HTMLResponse

# Initialize FastAPI app
app = FastAPI()


# Initialize database
Base.metadata.create_all(bind=engine)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-production-domain.com"],  # Specify actual origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specify allowed methods
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_base_router, prefix="/auth", tags=["auth"])
app.include_router(auth_routes.auth_router, prefix="/auth", tags=["auth_routes"])
app.include_router(facebook_auth.facebook_auth_router, prefix="/facebook", tags=["facebook_auth"])
app.include_router(ad_generation_routes.ad_generation_router, prefix="/ad-generation", tags=["ad_generation"])
app.include_router(ad_performance_routes.ad_performance_router, prefix="/ad-performance", tags=["ad_performance"])
app.include_router(media_assets.media_asset_router, prefix="/media-assets", tags=["media_assets"])
app.include_router(projects.projects_router, prefix="/projects", tags=["projects"])
app.include_router(users.users_router, prefix="/users", tags=["users"])


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Welcome to My FastAPI App</title>
        </head>
        <body>
            <h1>Welcome to My FastAPI Application!</h1>
            <p>This is a simple home page for your FastAPI app.</p>
            <p>Use the API endpoints provided to interact with the application.</p>
        </body>
    </html>
    """
    
# WebSocket Manager to handle connections
class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
        except Exception as e:
            print(f"Error connecting websocket: {e}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)
        
        # Clean up any disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

# Initialize WebSocket manager
manager = WebSocketManager()

# WebSocket route to handle connections
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client disconnected")

# Entry point to run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
