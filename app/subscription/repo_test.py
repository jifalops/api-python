from abc import ABC, abstractmethod

import pytest

from app.error import AppError
from app.subscription.models import (
    Customer,
    CustomerId,
    PriceId,
    Subscription,
    SubscriptionId,
    SubscriptionType,
)
from app.subscription.repo import SubscriptionRepo
from app.user.models import UserId


class SubscriptionRepoTest(ABC):

    @abstractmethod
    @pytest.fixture
    def repo(self) -> SubscriptionRepo:
        raise NotImplementedError()

    @pytest.fixture
    def customer(self) -> Customer:
        return Customer(id=CustomerId("cus_1"), user_id=UserId("user_1"))

    @pytest.fixture
    def customer2(self) -> Customer:
        return Customer(id=CustomerId("cus_2"), user_id=UserId("user_2"))

    @pytest.fixture
    def subscription_inactive(self, customer: Customer) -> Subscription:
        return Subscription(
            id=SubscriptionId("sub_1"),
            customer_id=customer.id,
            price_id=PriceId("price_1"),
            status="inactive",
            type=SubscriptionType(level="pro", period="annual", edition="founder"),
        )

    @pytest.fixture
    def subscription_active(self, customer2: Customer) -> Subscription:
        return Subscription(
            id=SubscriptionId("sub_2"),
            customer_id=customer2.id,
            price_id=PriceId("price_2"),
            status="active",
            type=SubscriptionType(level="pro", period="monthly", edition="founder"),
        )

    @pytest.mark.asyncio
    async def test_no_customers(self, repo: SubscriptionRepo, customer: Customer):
        with pytest.raises(AppError):
            await repo.get_customer_by_id(customer.id)

        with pytest.raises(AppError):
            await repo.get_customer_by_user_id(customer.user_id)

    @pytest.mark.asyncio
    async def test_create_customers(
        self, repo: SubscriptionRepo, customer: Customer, customer2: Customer
    ):
        await repo.create_customer(customer)
        with pytest.raises(AppError):
            await repo.create_customer(customer)

        await repo.create_customer(customer2)
        with pytest.raises(AppError):
            await repo.create_customer(customer2)

    @pytest.mark.asyncio
    async def test_read_customers(
        self, repo: SubscriptionRepo, customer: Customer, customer2: Customer
    ):
        await repo.create_customer(customer)
        assert await repo.get_customer_by_id(customer.id) == customer
        assert await repo.get_customer_by_user_id(customer.user_id) == customer

        await repo.create_customer(customer2)
        assert await repo.get_customer_by_id(customer2.id) == customer2
        assert await repo.get_customer_by_user_id(customer2.user_id) == customer2

    @pytest.mark.asyncio
    async def test_no_subscriptions(
        self, repo: SubscriptionRepo, subscription_inactive: Subscription
    ):
        with pytest.raises(AppError):
            await repo.get_subscription_by_id(subscription_inactive.id)

    @pytest.mark.asyncio
    async def test_create_subscriptions(
        self,
        repo: SubscriptionRepo,
        subscription_inactive: Subscription,
        subscription_active: Subscription,
    ):
        await repo.create_subscription(subscription_inactive)
        with pytest.raises(AppError):
            await repo.create_subscription(subscription_inactive)

        await repo.create_subscription(subscription_active)
        with pytest.raises(AppError):
            await repo.create_subscription(subscription_active)

    @pytest.mark.asyncio
    async def test_read_subscriptions(
        self,
        repo: SubscriptionRepo,
        subscription_inactive: Subscription,
        subscription_active: Subscription,
    ):
        await repo.create_subscription(subscription_inactive)
        assert (
            await repo.get_subscription_by_id(subscription_inactive.id)
            == subscription_inactive
        )

        await repo.create_subscription(subscription_active)
        assert (
            await repo.get_subscription_by_id(subscription_active.id)
            == subscription_active
        )

    @pytest.mark.asyncio
    async def test_update_subscriptions(
        self,
        repo: SubscriptionRepo,
        subscription_inactive: Subscription,
        subscription_active: Subscription,
    ):
        await repo.create_subscription(subscription_inactive)

        subscription_inactive.type.level = "plus"
        await repo.update_subscription(
            subscription_inactive.id, subscription_inactive.model_dump(mode="json")
        )
        assert (
            await repo.get_subscription_by_id(subscription_inactive.id)
            == subscription_inactive
        )

        subscription_inactive.status = "active"
        await repo.update_subscription(
            subscription_inactive.id, subscription_inactive.model_dump(mode="json")
        )
        assert (
            await repo.get_subscription_by_id(subscription_inactive.id)
            == subscription_inactive
        )

        await repo.create_subscription(subscription_active)
        subscription_active.status = "inactive"
        await repo.update_subscription(
            subscription_active.id, subscription_active.model_dump(mode="json")
        )
        assert (
            await repo.get_subscription_by_id(subscription_active.id)
            == subscription_active
        )

        with pytest.raises(AppError):
            await repo.update_subscription(
                subscription_inactive.id, subscription_active.model_dump(mode="json")
            )
