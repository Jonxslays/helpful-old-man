import miru

from hom.injector import Injector
from hom.services import EmbedService
from hom.views.base import ViewBase
from .utils import blue_button

__all__ = ("Groups",)


class Groups(ViewBase):
    @blue_button("Verify my group", "support-groups-verify")
    async def verify(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.verify_group(), button)

    @blue_button("Reset my verification code", "support-groups-reset")
    async def reset(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.reset_group_code(), button)

    @blue_button("Remove me from a group", "support-groups-remove")
    async def remove(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.remove_from_group(), button)

    @blue_button("Other", "support-groups-other")
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.other(), button)
