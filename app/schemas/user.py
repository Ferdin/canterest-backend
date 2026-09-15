from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str
    username: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    name: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True

class PublicUserOut(BaseModel):
    id: int
    username: str
    name: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True

class MeOut(BaseModel):
    authorized: bool
    user: UserOut | None = None        