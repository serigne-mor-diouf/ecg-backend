import smtplib
from email.message import EmailMessage

from app.core.config import settings


def envoyer_email(destinataire: str, sujet: str, corps: str) -> None:
    message = EmailMessage()
    message["From"] = settings.mail_sender
    message["To"] = destinataire
    message["Subject"] = sujet
    message.set_content(corps)

    with smtplib.SMTP(settings.mail_host, settings.mail_port) as smtp:
        smtp.starttls()
        smtp.login(settings.mail_username, settings.mail_password)
        smtp.send_message(message)


def envoyer_code_reinitialisation(destinataire: str, code: str) -> None:
    envoyer_email(
        destinataire,
        sujet="Réinitialisation de votre mot de passe - ECG Backend",
        corps=(
            f"Bonjour,\n\n"
            f"Voici votre code de validation pour réinitialiser votre mot de passe : {code}\n"
            f"Ce code est valable 30 minutes.\n\n"
            f"Si vous n'êtes pas à l'origine de cette demande, ignorez cet email."
        ),
    )
