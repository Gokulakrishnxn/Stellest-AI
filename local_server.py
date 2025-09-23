from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
import os

# Import sub-apps
from api.predict import app as predict_app
from api.health import app as health_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="Stellest AI - Local Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>index.html not found</h1>")

@app.get("/signin", response_class=HTMLResponse)
async def signin():
    page = os.path.join(BASE_DIR, "signin.html")
    if os.path.exists(page):
        with open(page, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>signin.html not found</h1>")

@app.get("/signup", response_class=HTMLResponse)
async def signup():
    page = os.path.join(BASE_DIR, "signup.html")
    if os.path.exists(page):
        with open(page, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>signup.html not found</h1>")

@app.get("/firebase-config.js")
async def firebase_config():
    path = os.path.join(BASE_DIR, "firebase-config.js")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return PlainTextResponse(f.read(), media_type="application/javascript")
    return PlainTextResponse("window.FIREBASE_CONFIG=null;", media_type="application/javascript")

@app.get("/supabase-config.js")
async def supabase_config():
    path = os.path.join(BASE_DIR, "supabase-config.js")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return PlainTextResponse(f.read(), media_type="application/javascript")
    return PlainTextResponse("window.SUPABASE_CONFIG=null;", media_type="application/javascript")

# Mount API apps under /api/* like Vercel
app.mount("/api/predict", predict_app)
app.mount("/api/health", health_app)
