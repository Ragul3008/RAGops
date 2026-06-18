import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from app.services.auth_service import AuthService
from app.domain.entities import User, UserRole
from app.schemas.auth import LoginRequest

@pytest.fixture
def mock_user_repo():
    return AsyncMock()

@pytest.fixture
def mock_token_store():
    return AsyncMock()

@pytest.mark.asyncio
async def test_authenticate_success(
    mock_user_repo, mock_token_store
):
    user = User(email="a@b.com", hashed_password="hashed_password") # User model constructor might need password/tenant_id
    mock_user_repo.find_by_email.return_value = user
    svc = AuthService(mock_user_repo, mock_token_store)
    
    # We need to mock verify_password to return True for the test
    # Let's import patch or mock it directly if needed, or set User's hashed_password using pwd_context.hash("secret")
    from app.core.security import get_password_hash
    user.hashed_password = get_password_hash("secret")
    user.tenant_id = uuid4()
    user.id = uuid4()
    user.roles = [UserRole.MEMBER]
    
    result = await svc.authenticate(
        LoginRequest(email="a@b.com",
                     password="secret",
                     tenant_id=user.tenant_id)
    )
    assert result.access_token is not None