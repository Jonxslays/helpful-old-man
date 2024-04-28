import hikari
import miru

from hom.injector import Injector
from hom.services import TicketService

__all__ = ("Archive",)


class Archive(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(
        label="Archive Ticket",
        emoji="\N{CROSS MARK}",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="ticket-archive",
    )
    async def close_ticket(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        tickets = Injector.get(TicketService)

        await tickets.archive(ctx)
