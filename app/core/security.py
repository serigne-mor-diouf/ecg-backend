import secrets
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(mot_de_passe: str) -> str:
    hashed = bcrypt.hashpw(mot_de_passe.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verifier_mot_de_passe(mot_de_passe: str, mot_de_passe_hash: str) -> bool:
    return bcrypt.checkpw(mot_de_passe.encode("utf-8"), mot_de_passe_hash.encode("utf-8"))


def creer_access_token(sub: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": sub, "role": role, "exp": expire, "jti": uuid.uuid4().hex}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decoder_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def generer_code_validation() -> str:
    """Code numérique à 6 chiffres, à envoyer par email pour la réinitialisation."""
    return f"{secrets.randbelow(1_000_000):06d}"
