from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    default_admin_email: str = "admin@ecg.com"
    default_admin_password: str = "Admin1234"
    default_admin_nom: str = "Admin"
    default_admin_prenom: str = "Systeme"

    mail_host: str = "smtp.gmail.com"
    mail_port: int = 587
    mail_username: str
    mail_password: str
    mail_sender: str

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
