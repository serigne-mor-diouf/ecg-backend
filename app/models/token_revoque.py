from sqlalchemy import Column, DateTime, String
from app.database import Base


class TokenRevoque(Base):
    """Liste noire des tokens JWT invalidés par un logout avant leur expiration naturelle."""

    __tablename__ = "tokens_revoques"

    jti = Column(String, primary_key=True)
    expire_at = Column(DateTime(timezone=True), nullable=False)
