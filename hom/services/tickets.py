import hikari

from hom.injector import Injector
from hom.models import Ticket
from .embeds import EmbedService

__all__ = ("TicketService",)


class TicketService:
    __slots__ = ()

    async def create(self, interaction: hikari.ComponentInteraction) -> None:
        embeds = Injector.get(EmbedService)

        if ticket := await self.get_ticket(interaction.user):
            # Already has an open ticket
            message = f":envelope: Click [here](<#{ticket.channel}>) to view your open ticket."
            return await interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embeds.info(message),
                flags=hikari.MessageFlag.EPHEMERAL,
            )

        # TODO: Continue this

        return None

    async def get_ticket(self, user: hikari.User) -> Ticket | None:
        return None
