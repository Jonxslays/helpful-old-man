import hikari
import miru

from hom.injector import Injector
from hom.services import TicketService
from hom.services import EmbedService
from . import ApiKey
from . import Other

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
    async def patreon(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed PATREON", components=self)
        print("Clicks patreon")

    @miru.button(label="API Key", custom_id="support-api-key", style=hikari.ButtonStyle.SUCCESS)
    async def api_key(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        tickets = Injector.get(TicketService)

        await tickets.create(ctx, embeds.api_key(), ApiKey(), str(button.label))

    @miru.button(label="Other", custom_id="support-other", style=hikari.ButtonStyle.SUCCESS)
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        tickets = Injector.get(TicketService)

        await tickets.create(ctx, embeds.other(), Other(), str(button.label))
