import hikari
import miru

from hom.injector import Injector
from hom.services import TicketService
from hom.services import EmbedService
from . import Closable

__all__ = ("Support",)


class Support(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(label="Groups", custom_id="support-groups", style=hikari.ButtonStyle.SUCCESS)
    async def groups(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed GROUPS", components=self)
        print("Clicks groups")

    @miru.button(label="Name Changes", custom_id="support-names", style=hikari.ButtonStyle.SUCCESS)
    async def names(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed NAMES", components=self)
        print("Clicks names")

    @miru.button(label="Patreon", custom_id="support-patreon", style=hikari.ButtonStyle.SUCCESS)
    async def patreon(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.patreon(), button)

    @miru.button(label="API Key", custom_id="support-api-key", style=hikari.ButtonStyle.SUCCESS)
    async def api_key(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.api_key(), button)

    @miru.button(label="Other", custom_id="support-other", style=hikari.ButtonStyle.SUCCESS)
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.other(), button)

    async def closable_ticket(
        self, ctx: miru.ViewContext, embed: hikari.Embed, button: miru.Button
    ) -> None:
        tickets = Injector.get(TicketService)
        await tickets.create(ctx, embed, Closable(), str(button.label))
