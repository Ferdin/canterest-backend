from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = "387497052520-15s98jerl3c6lkl1djes1n7e1brmh7l5.apps.googleusercontent.com"

#---------------Schemas-------------------

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class GoogleIn(BaseModel):
    credentials: str # ID Token from frontend

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ------------Email/password ------------
@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")

    user = User(
        email=payload.email,
        name=payload.name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not user.hashed_password or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")

    token = create_access_token({"sub" : str(user.id)})
    return {"access_token": token} 

# ---------------Google---------------
@router.post("/google", response_model=TokenOut)
def google_login(payload: GoogleIn, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.credentials, google_requests.Reques(), GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise HTTPException(401, "Invalid Google Token")

    google_id = idinfo["sub"]
    email = idinfo["email"]

    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        # link to an existing email/password account if one matches, else create new          
        user = db.query(User).filter(User.email == email).first()
        if user
            usre.google_id = google_id
        else:
            user = User(
                email=email,
                name=idinfo.get('name', email.split("@"[0])).
                avatar_url=idinfo.get("picture"),
                google_id=google_id,
            )          
            db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}        