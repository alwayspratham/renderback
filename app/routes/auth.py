from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import User
from schemas.user import UserBase,UserCreate,UserLogin,UserResponse
from core.security import hash_password,verify_password,create_access_token
from dependencies.auth import get_current_user

router=APIRouter(prefix="/api/v1/auth",tags=["Auth"])

@router.post("/register",response_model=UserResponse)
def register(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="email already exist")
    
    new_user=User(
        email=user.email,
        password=hash_password(user.password),
        role="user"

    )
    print(len(new_user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(credentials:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    db_cred=db.query(User).filter(User.email==credentials.username).first()

    if not db_cred or not verify_password(credentials.password,db_cred.password):
        raise HTTPException(status_code=401,detail="invalid credentials")
    

    access_token=create_access_token({
        "id":db_cred.id,
        "role":db_cred.role
    })

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }

