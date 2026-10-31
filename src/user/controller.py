from fastapi import HTTPException, status, Request, BackgroundTasks
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.settings import settings
from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.mail import send_email

get_password_hash = PasswordHash.recommended().hash


def verify_password(unhashed_password, hashed_password):
    return PasswordHash.recommended().verify(unhashed_password, hashed_password)

async def register(body:UserSchema,bg_task:BackgroundTasks , db:Session):

    user_exist = db.query(UserModel).filter(UserModel.username == body.username).first()

    if user_exist:
        raise HTTPException(400, detail="User already taken")

    email_exist = db.query(UserModel).filter(UserModel.email == body.email).first()

    if email_exist:
        raise HTTPException(400, detail="Email already registered")

    password_hash = get_password_hash(body.password)

    new_user = UserModel(

        name = body.name,
        username = body.username,
        password_hash = password_hash,
        email = body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # send mail
    # res = await send_email([new_user.email],body.name, body.username, body.password)
    bg_task.add_task(send_email, [new_user.email],body.name, body.username, body.password)
    # print(res)

    return new_user



def login_user(body:LoginSchema, db:Session):

    user_exist = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username")

    if not verify_password(body.password, user_exist.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")

    time_to_token_expiry = datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRY_TIME) #minutes=settings.TOKEN_EXPIRY_TIME

    token = jwt.encode({"_id":user_exist.id, "expiry":time_to_token_expiry.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)
    
    # print(body)
    # return "logged in"

    return token

# token auth
def is_auth(request:Request, db:Session):
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
