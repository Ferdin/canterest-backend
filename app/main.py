from fastapi import FastAPI
from routers import auth  # Import your router file

app = FastAPI()

# Include the router into the main app
app.include_router(auth.router)