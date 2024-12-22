from app.subscription.models import Customer, CustomerId, SubscriptionId


class SubscriptionRepo:
    async def create_customer(self, customer: Customer) -> None:
        pass

    async def set_subscription_id(
        self, customer_id: CustomerId, subscription_id: SubscriptionId | None
    ) -> None:
        pass
