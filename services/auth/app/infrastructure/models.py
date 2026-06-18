from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.infrastructure.database import Base

class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        {"schema": "auth"},
    )
    
    id: Column = Column(UUID(as_uuid=True), primary_key=True)
    email: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)
    tenant_id: Column = Column(UUID(as_uuid=True), index=True)
    roles: Column = Column(ARRAY(String), default=[])
    is_active: Column = Column(Boolean, default=True)

    
    def to_domain(self):
        from app.domain.entities import User, UserRole
        return User(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            tenant_id=self.tenant_id,
            roles=[UserRole(r) for r in self.roles] if self.roles else [],
            is_active=self.is_active,
        )