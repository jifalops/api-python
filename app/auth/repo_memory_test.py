import pytest

from app.auth.models import (
    AuthInvalidUpdateError,
    AuthUser,
    AuthUserAlreadyExistsError,
    AuthUserNotFoundError,
    UserId,
)
from app.auth.repo import AuthRepo
from app.auth.repo_memory import AuthRepoMemory


@pytest.fixture
def repo() -> AuthRepo:
    return AuthRepoMemory()


@pytest.fixture
def user() -> AuthUser:
    return AuthUser(id=UserId("user_1"))


@pytest.fixture
def user2() -> AuthUser:
    return AuthUser(id=UserId("user_2"))


@pytest.mark.asyncio
async def test_no_users(repo: AuthRepo, user: AuthUser):
    with pytest.raises(AuthUserNotFoundError):
        await repo.get_user_by_id(user.id)

    with pytest.raises(AuthUserNotFoundError):
        await repo.update_user(user.id, user.model_dump(mode="json"))

    with pytest.raises(AuthUserNotFoundError):
        await repo.delete_user(user.id)

    assert await repo.is_only_user(user.id) == False


@pytest.mark.asyncio
async def test_create_users(repo: AuthRepo, user: AuthUser, user2: AuthUser):
    await repo.create_user(user)
    with pytest.raises(AuthUserAlreadyExistsError):
        await repo.create_user(user)
    assert await repo.is_only_user(user.id) == True

    await repo.create_user(user2)
    with pytest.raises(AuthUserAlreadyExistsError):
        await repo.create_user(user2)
    assert await repo.is_only_user(user.id) == False
    assert await repo.is_only_user(user2.id) == False


@pytest.mark.asyncio
async def test_read_users(repo: AuthRepo, user: AuthUser, user2: AuthUser):
    await repo.create_user(user)
    assert await repo.get_user_by_id(user.id) == user

    await repo.create_user(user2)
    assert await repo.get_user_by_id(user2.id) == user2

    assert await repo.get_user_by_id(user.id) == user


@pytest.mark.asyncio
async def test_update_users(repo: AuthRepo, user: AuthUser, user2: AuthUser):
    user.email = None
    await repo.create_user(user)

    user.email = "a@b.c"
    await repo.update_user(user.id, user.model_dump(mode="json"))
    assert await repo.get_user_by_id(user.id) == user

    user.email = None
    await repo.update_user(user.id, user.model_dump(mode="json"))
    assert user == await repo.get_user_by_id(user.id)

    user2.phone = None
    await repo.create_user(user2)

    user2.phone = "1234567890"
    await repo.update_user(user2.id, user2.model_dump(mode="json"))
    assert user2 == await repo.get_user_by_id(user2.id)

    user2.phone = None
    await repo.update_user(user2.id, user2.model_dump(mode="json"))
    assert user2 == await repo.get_user_by_id(user2.id)

    with pytest.raises(AuthInvalidUpdateError):
        await repo.update_user(user.id, user2.model_dump(mode="json"))
