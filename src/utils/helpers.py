from fastapi import HTTPException, status, Request, Depends
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils.db import get_db
from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError


# token auth
def is_auth(request:Request, db:Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
        
        token = token.split(" ")[-1]


        # this uses public key cryptography the jwt secret key is private key!!
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

        id = data.get("_id")
        expiry = data.get("expiry")

        current_time = datetime.now().timestamp()

        if current_time > expiry:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")

        user_exist = db.query(UserModel).filter(UserModel.id == id).first()
        
        if not user_exist:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
        
        
        return user_exist
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
