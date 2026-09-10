from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, uploads, pins  # Import your router file
from fastapi.staticfiles import StaticFiles 

app = FastAPI()

# Include the router into the main app

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(pins.router)