from abc import ABC, abstractmethod

import pytest

from app.user.models import (
    FullUser,
    User,
    UserAlreadyExistsError,
    UserId,
    UserInvalidUpdateError,
    UserNotFoundError,
)
from app.user.repo import UserRepo


class UserRepoTest(ABC):

    @abstractmethod
    @pytest.fixture
    def repo(self) -> UserRepo:
        raise NotImplementedError()

    @pytest.fixture
    def user(self) -> FullUser:
        return FullUser(id=UserId("user_1"))

    @pytest.fixture
    def user2(self) -> FullUser:
        return FullUser(id=UserId("user_2"))

    @pytest.mark.asyncio
    async def test_no_users(self, repo: UserRepo, user: User):
        with pytest.raises(UserNotFoundError):
            await repo.get_user_by_id(user.id)

        with pytest.raises(UserNotFoundError):
            await repo.update_user(user.id, user.model_dump(mode="json"))

        with pytest.raises(UserNotFoundError):
            await repo.delete_user(user.id)

    @pytest.mark.asyncio
    async def test_create_users(self, repo: UserRepo, user: User, user2: User):
        await repo.create_user(user)
        with pytest.raises(UserAlreadyExistsError):
            await repo.create_user(user)

        await repo.create_user(user2)
        with pytest.raises(UserAlreadyExistsError):
            await repo.create_user(user2)

    @pytest.mark.asyncio
    async def test_read_users(self, repo: UserRepo, user: User, user2: User):
        await repo.create_user(user)
        assert await repo.get_user_by_id(user.id) == user

        await repo.create_user(user2)
        assert await repo.get_user_by_id(user2.id) == user2

        assert await repo.get_user_by_id(user.id) == user

    @pytest.mark.asyncio
    async def test_update_users(self, repo: UserRepo, user: User, user2: User):
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

        user2.phone = "+15555555555"
        await repo.update_user(user2.id, user2.model_dump(mode="json"))
        assert user2 == await repo.get_user_by_id(user2.id)

        user2.phone = None
        await repo.update_user(user2.id, user2.model_dump(mode="json"))
        assert user2 == await repo.get_user_by_id(user2.id)

        with pytest.raises(UserInvalidUpdateError):
            await repo.update_user(user.id, user2.model_dump(mode="json"))

    @pytest.mark.asyncio
    async def test_delete_users(self, repo: UserRepo, user: User, user2: User):
        await repo.create_user(user)
        await repo.create_user(user2)

        await repo.delete_user(user.id)

        with pytest.raises(UserNotFoundError):
            await repo.get_user_by_id(user.id)
        assert await repo.get_user_by_id(user2.id) == user2

        await repo.delete_user(user2.id)
        with pytest.raises(UserNotFoundError):
            await repo.get_user_by_id(user2.id)

        with pytest.raises(UserNotFoundError):
            await repo.delete_user(user.id)

        with pytest.raises(UserNotFoundError):
            await repo.delete_user(user2.id)
