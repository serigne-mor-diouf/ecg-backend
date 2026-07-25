from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.token_revoque import TokenRevoque


def revoquer(db: Session, jti: str, expire_at: datetime) -> None:
    db.add(TokenRevoque(jti=jti, expire_at=expire_at))
    db.commit()


def est_revoque(db: Session, jti: str) -> bool:
    return db.query(TokenRevoque).filter(TokenRevoque.jti == jti).first() is not None


def purger_tokens_expires(db: Session) -> None:
    db.query(TokenRevoque).filter(TokenRevoque.expire_at < datetime.now(timezone.utc)).delete()
    db.commit()
