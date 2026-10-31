from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from src.utils.settings import settings

# class EmailSchema(BaseModel):
#     email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME="Thetscloud@gmail.com",
    MAIL_PASSWORD=settings.MAIL_PASS,
    MAIL_FROM="Thetscloud@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Thetscloud",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True

)


async def send_email(emails: List[str], name:str, username:str, password:str):
    html = f"""<p>Hey there {name}, Thanks for registering with Thetscloud! </p>
        <br> <p>Your Registered Login credentials are:</p>
        <p>Username: {username} </p>
        <p>Password: {password}</p>
        """

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message":"mail sent"}