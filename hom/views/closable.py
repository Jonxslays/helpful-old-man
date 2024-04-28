import hikari
import miru

from hom.injector import Injector
from hom.services import TicketService
from . import Archive

__all__ = ("Closable",)


class Closable(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(
        label="Close",
        emoji="\N{LOCK}",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="ticket-close",
    )
    async def close_ticket(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        tickets = Injector.get(TicketService)

        await tickets.close(ctx, Archive())
