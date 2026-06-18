from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class UserRole(Enum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN   = "org_admin"
    MEMBER      = "member"
    VIEWER      = "viewer"

@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    email: str = ""
    hashed_password: str = ""
    tenant_id: UUID | None = None

    roles: list[UserRole] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(
        default_factory=datetime.utcnow
    )
    
    def has_role(self, role: UserRole) -> bool:
        return role in self.roles