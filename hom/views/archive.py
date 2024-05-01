import hikari
import miru

from hom.injector import Injector
from hom.services import TicketService
from hom.views.base import ViewBase

__all__ = ("Archive",)


class Archive(ViewBase):
    @miru.button(
        label="Archive Ticket",
        emoji="\N{CROSS MARK}",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="ticket-archive",
    )
    async def archive_ticket(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        tickets = Injector.get(TicketService)

        await tickets.archive(ctx)
