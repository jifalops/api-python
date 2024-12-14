from abc import abstractmethod

from app.service import Service
from app.subscription_portal.models import BillingManage, CheckoutStart, SessionInfo
from app.user.models import User


class SubscriptionPortalService(Service):

    @abstractmethod
    async def start_checkout(self, user: User, data: CheckoutStart) -> SessionInfo:
        raise NotImplementedError()

    @abstractmethod
    async def manage_billing(self, user: User, data: BillingManage) -> SessionInfo:
        raise NotImplementedError()
