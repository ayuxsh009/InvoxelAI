from datetime import datetime

from app.models.user import UserRole
from app.schemas.common import ORMModel


class UserOut(ORMModel):
    id: int
    name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
