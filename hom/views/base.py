import hikari
import miru

from hom.injector import Injector
from hom.services import TicketService
from hom.views.ticket import Ticket

__all__ = ("ViewBase",)


class ViewBase(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def closable_ticket(
        self, ctx: miru.ViewContext, embed: hikari.Embed, button: miru.Button
    ) -> None:
        """Creates a new support ticket with a close button.

        Args:
            ctx: The miru view context.
            embed: The embed to send in the initial ticket message.
            button: The button that was clicked to open this ticket.
        """
        tickets = Injector.get(TicketService)
        await tickets.create(ctx, embed, Ticket(), str(button.label))

    async def ephemeral_view(
        self, ctx: miru.ViewContext, view: miru.View, message: str | None = None
    ) -> None:
        """Creates a new ephemeral view in response to this interaction.

        If no message is supplied, the default message is:

        `What do you need assistance with?`

        Args:
            ctx: The miru view context.
            view: The view to send.
            message: The optional text to send with the view.
        """
        await ctx.respond(
            message or "What do you need assistance with?",
            flags=hikari.MessageFlag.EPHEMERAL,
            components=view,
        )
