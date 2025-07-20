from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db.database import get_session
from auth import models, schemas, auth_utils

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=schemas.Token)
def signup(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(models.User).where(models.User.username == user.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    hashed_pw = auth_utils.hash_password(user.password)
    access_token = auth_utils.create_access_token({"username": user.username})
    refresh_token = auth_utils.create_refresh_token({"username": user.username})
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        current_acccess_token=access_token,
        current_refresh_token=refresh_token,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(
        select(models.User).where(models.User.username == user.username)
    ).first()

    if not db_user or not auth_utils.verify_password(
        user.password, db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = auth_utils.create_access_token({"username": db_user.username})
    refresh_token = auth_utils.create_refresh_token({"username": db_user.username})
    db_user.current_acccess_token = access_token
    db_user.current_refresh_token = refresh_token
    session.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=schemas.AccessTokenOnly)
def refresh_token(
    refresh_payload: schemas.RefreshToken,  # takes `refresh_token: str`
    session: Session = Depends(get_session),
):
    decoded_payload = auth_utils.decode_token(refresh_payload.refresh_token)
    username = decoded_payload.get("username")
    token_type = decoded_payload.get("type")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if token_type != "refresh":
        raise HTTPException(status_code=401, detail="Provide a valid refresh Token")
    user = session.exec(
        select(models.User).where(models.User.username == username)
    ).first()

    if user.current_refresh_token != refresh_payload.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is expired")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = auth_utils.create_access_token({"username": user.username})
    user.current_acccess_token = new_access_token
    session.commit()
    return {"access_token": new_access_token}


@router.get("/me")
def get_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return {"username": current_user.username, "email": current_user.email}
