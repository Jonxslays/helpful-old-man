import miru

from hom.injector import Injector
from hom.services import EmbedService
from hom.views.base import ViewBase
from .groups import Groups
from .names import Names
from .utils import green_button

__all__ = ("Support",)


class Support(ViewBase):
    """The view containing the buttons for the support embed.

    These buttons are used for opening support tickets.
    """

    @green_button("Groups", "support-groups")
    async def groups(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        await self.ephemeral_view(ctx, Names())

    @green_button("Name Changes", "support-names")
    async def names(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        await self.ephemeral_view(ctx, Groups())

    @green_button("Patreon", "support-patreon")
    async def patreon(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.patreon(), button)

    @green_button("API Key", "support-api-key")
    async def api_key(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.api_key(), button)

    @green_button("Other", "support-other")
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.other(), button)
