import hikari
import miru

from hom.injector import Injector
from hom.services import TicketService
from hom.views import ViewBase
from .archive import Archive

__all__ = ("Ticket",)


class Ticket(ViewBase):
    """Consists of a single button "Close" for closing a ticket.

    Clicking the button will remove permissions from the original owner
    and update the ticket channel topic to be suffixed with _CLOSED.
    """

    @miru.button(
        label="Close",
        emoji="\N{LOCK}",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="ticket-close",
    )
    async def close_ticket(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        tickets = Injector.get(TicketService)
        await tickets.close(ctx, Archive())
