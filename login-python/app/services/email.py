from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Usar MAIL_STARTTLS en vez de MAIL_TLS
    MAIL_SSL_TLS=False,  # Usar MAIL_SSL_TLS en vez de MAIL_SSL
    USE_CREDENTIALS=True
)

async def send_reset_email(email: str, reset_token: str):
    reset_url = f"http://localhost:3000/auth/reset-password?token={reset_token}"
    message = MessageSchema(
        subject="Recuperación de contraseña",
        recipients=[email],
        body=f"""
        <h3>Recuperación de contraseña</h3>
        <p>Haga clic en el siguiente enlace para restablecer su contraseña:</p>
        <a href="{reset_url}">{reset_url}</a>
        <p>Este enlace expirará en 30 minutos.</p>
        """,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
