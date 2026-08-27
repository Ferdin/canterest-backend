from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True

class MeOut(BaseModel):
    authorized: bool
    user: UserOut | None = None        