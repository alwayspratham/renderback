from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from jose import jwt,JWTError
from core import security
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,security.SECRECT_KEY,security.ALGORITHM)
        user_id=payload.get("id")
        role=payload.get("role")
        
        if user_id is None:
            raise HTTPException(status_code=401,detail="Invalid  token")
        return {"id":user_id,"role":role}
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid or expired token")
    
def get_cuurent_admin(user=Depends(get_current_user)):
    if user['role']!="admin":
        raise HTTPException(status_code=403,detail="Admin access required")
    return user


        