import utils.http_session
import utils.transport
import utils.session
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://particlesolar.in",  # your React app URL
    # Add other origins if needed
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email configuration - use your SMTP details here
conf = ConnectionConfig(
    MAIL_USERNAME="particlesolar@gmail.com",
    MAIL_PASSWORD="rftn kxlb iwsp aqea",
    MAIL_FROM="particlesolar@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,    # instead of MAIL_TLS
    MAIL_SSL_TLS=False,    # instead of MAIL_SSL
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class EmailSchema(BaseModel):
    name: str
    org: str
    email: EmailStr
    phone: str
    message: str


@app.get("/")
async def root():
    return {"message":"fastAPI backend is running!"}

@app.post("/send-mail")
async def send_mail(email: EmailSchema):
    message = MessageSchema(
        subject="New Form Submission",
        recipients=["particlesolar@gmail.com"],  # your receiving email
        body=f"""
        Name: {email.name}
        Organization: {email.org}
        Email: {email.email}
        Phone: {email.phone}
        Message: {email.message}
        """,
        subtype="plain"
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
