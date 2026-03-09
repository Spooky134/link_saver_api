import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.repositories import UserRepository


@pytest.mark.parametrize("email, is_present", [
    ("alice.smith@example.com", True),
    ("alice.smith@test.com", False),
])
async def test_get_by_email(email: str, is_present: bool, db_session: AsyncSession):
    user_repo = UserRepository(db_session)
    user = await user_repo.get_by_email(email)

    if is_present:
        assert user
        assert user.email == email
    else:
        assert not user
