from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db.models.users import User
from db.config import get_session
from db.schemas.users import CreateUser
from db.security import pwd_context

router = APIRouter(prefix="/api/v1/signup", tags=["SignUp"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def create_user(
    user: CreateUser,
    db: Session = Depends(get_session),
):
    existing_username = db.exec(
        select(User).where(User.username == user.username)
    ).first()
    existing_email = db.exec(select(User).where(User.email == user.email)).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist"
        )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @router.get("/")
# async def get_users() -> List[User]:
#     users = session.exec(select(User)).all()
#     return users
