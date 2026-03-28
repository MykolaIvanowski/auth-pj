from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from db.session import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    revoke = Column(Boolean, deafault=False)