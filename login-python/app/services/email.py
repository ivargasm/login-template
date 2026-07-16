import resend
from app.config import RESEND_API_KEY, RESEND_MAIL_FROM, URL_FRONT

resend.api_key = RESEND_API_KEY

def get_reset_password_html(reset_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recuperación de Contraseña</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #f4f7fa;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }}
            .email-header {{
                background-color: #007bff;
                color: #ffffff;
                text-align: center;
                padding: 30px 20px;
            }}
            .email-header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 600;
            }}
            .email-body {{
                padding: 40px 30px;
                color: #333333;
                line-height: 1.6;
            }}
            .email-body p {{
                font-size: 16px;
                margin-bottom: 20px;
            }}
            .btn-container {{
                text-align: center;
                margin: 30px 0;
            }}
            .btn {{
                background-color: #007bff;
                color: #ffffff !important;
                text-decoration: none;
                padding: 14px 28px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                display: inline-block;
            }}
            .email-footer {{
                background-color: #f8f9fa;
                text-align: center;
                padding: 20px;
                color: #777777;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>Recuperación de Contraseña</h1>
            </div>
            <div class="email-body">
                <p>Hola,</p>
                <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta. Si fuiste tú, por favor haz clic en el botón de abajo para asignar una nueva contraseña:</p>
                
                <div class="btn-container">
                    <a href="{reset_url}" class="btn">Restablecer mi contraseña</a>
                </div>
                
                <p>Si el botón no funciona, también puedes copiar y pegar el siguiente enlace en tu navegador:</p>
                <p><a href="{reset_url}" style="color: #007bff; word-break: break-all;">{reset_url}</a></p>
                
                <p><strong>Nota:</strong> Este enlace expirará en 30 minutos por razones de seguridad.</p>
                <p>Si no solicitaste este cambio, puedes ignorar este mensaje tranquilamente. Tu contraseña actual seguirá siendo la misma.</p>
            </div>
            <div class="email-footer">
                <p>&copy; 2026 Tu Aplicación. Todos los derechos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """

async def send_reset_email(email: str, reset_token: str):
    # Asegúrate de usar la URL_FRONT del config para armar la url final
    reset_url = f"{URL_FRONT}/auth/reset-password?token={reset_token}"
    
    html_content = get_reset_password_html(reset_url)

    params = {
        "from": RESEND_MAIL_FROM or "onboarding@resend.dev",
        "to": [email],
        "subject": "Solicitud para restablecer tu contraseña",
        "html": html_content
    }

    try:
        # Enviar el correo usando Resend
        email_response = resend.Emails.send(params)
        print("Email enviado con éxito:", email_response)
    except Exception as e:
        print("Error enviando el correo con Resend:", str(e))
