import miru

from hom.injector import Injector
from hom.services import EmbedService
from hom.views.base import ViewBase
from .utils import blue_button

__all__ = ("Names",)


class Names(ViewBase):
    @blue_button("Approve a pending name change", "support-names-approve")
    async def approve(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.approve_name_change(), button)

    @blue_button("Delete name change history", "support-names-delete")
    async def review(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.delete_name_changes(), button)

    @blue_button("Review a denied name change", "support-names-review")
    async def delete(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.review_name_change(), button)

    @blue_button("Other", "support-names-other")
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.other(), button)
