from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select

from pwdlib import PasswordHash

from validation import USER, API
from database import get_db, user_info
from auth import create_access_token, verify_access_token


app = FastAPI()

p = PasswordHash.recommended()

security = HTTPBearer()


# CORS CONFIGURATION

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# REGISTER

@app.post("/register", response_model=API)
def register(user: USER, db=Depends(get_db)):

    new_user = user_info(
        name=user.name,
        pas=p.hash(user.pas)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# LOGIN

@app.post("/login")
def login(user: USER, db=Depends(get_db)):

    statement = select(user_info).where(
        user_info.name == user.name
    )

    result = db.execute(statement)
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not p.verify(user.pas, existing_user.pas):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = create_access_token(existing_user.id)

    return {45
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# GET CURRENT USER

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):

    # 1. Extract JWT
    token = credentials.credentials

    # 2. Verify JWT
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # 3. Extract user ID
    subject = payload.get("sub")

    try:
        user_id = int(subject)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token subject"
        )

    # 4. Fetch user from PostgreSQL
    statement = select(user_info).where(
        user_info.id == user_id
    )

    result = db.execute(statement)
    current_user = result.scalars().first()

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User does not exist"
        )

    # 5. Return authenticated user
    return current_user


# PERSONALIZED DASHBOARD

@app.get("/dashboard")
def dashboard(
    current_user=Depends(get_current_user)
):

    return {
        "message": "Welcome to your dashboard",
        "user_id": current_user.id,
        "name": current_user.name
    }