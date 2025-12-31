from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import agent

app = FastAPI(title="CogniCode AI API")

# מאפשר לפרונטנד (localhost:5173) לדבר עם הבקנד
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# מחבר את ה-Routes של הסוכנים
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is live"}