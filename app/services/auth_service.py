import re 
from app.core.constants import RESERVED_USERNAMES

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,20}$")

def validate_username(username: str) -> None:
    if not USERNAME_PATTERN.match(username):
        raise ValueError(
            "Username must be 3-20 characters and contain only letters, numbers, and underscores"
        )
    if username.lower() in RESERVED_USERNAMES:
        raise ValueError("This username is not available")

def generate_username_from_email(db:Session, email: str) -> str:
    # take the part before @, strip anything that isn't letter/number/underscore
    base = re.sub(r"[^a-zA-Z0-9_]", "", email.split("@")[0].lower())       

    # enforce minimum length (pad if too short after stripping)
    if len(base) < 3:
        base = (base + "user")[:20]

    base = base[:17]  # leave room for a numeric suffix, keep under 20 total

    candidate = base
    suffix = 0

    while (
        candidate.lower() in RESERVED_USERNAMES
        or db.query(User).filter(User.username == candidate).first()
    ):
        suffix += 1
        candidate = f"{base}{suffix}"

    return candidate
    
def register_user(db: Session, email: str, password: str, name: str, username: str) -> str:
    validate_username(username)
    
    if db.query(User).filter(User.email ==  email).first():
        raise ValueError("Email already registered")
    if db.query(User).filter(User.username == username).first():
        raise ValueError("Username already taken")

    user = User(
        email=email,
        name=name,
        username=username,
        hashed_password=hashed_password(password),
    )    
    db.add(user)
    db.commit()
    db.refresh(user)
    return create_access_token({"sub": str(user.id)})