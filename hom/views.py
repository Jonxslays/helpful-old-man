# import functools
# import typing as t

import hikari
import miru

from hom.injector import Injector
from hom.services import EmbedService
from hom.services import TicketService

__all__ = ("Archive", "Groups", "Names", "Support", "Ticket", "ViewBase")


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


class Groups(ViewBase):
    @miru.button(
        label="Verify my group",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-groups-verify",
    )
    async def verify(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.verify_group(), button)

    @miru.button(
        label="Reset my verification code",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-groups-reset",
    )
    async def reset(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.reset_group_code(), button)

    @miru.button(
        label="Remove me from a group",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-groups-remove",
    )
    async def remove(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.remove_from_group(), button)

    @miru.button(
        label="Other",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-groups-other",
    )
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.other(), button)


class Names(ViewBase):
    @miru.button(
        label="Approve a pending name change",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-names-approve",
    )
    async def approve(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.approve_name_change(), button)

    @miru.button(
        label="Delete name change history",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-names-delete",
    )
    async def review(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.delete_name_changes(), button)

    @miru.button(
        label="Review a denied name change",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-names-review",
    )
    async def delete(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.review_name_change(), button)

    @miru.button(
        label="Other",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-names-other",
    )
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.other(), button)


class Support(ViewBase):
    """The view containing the buttons for the support embed.

    These buttons are used for opening support tickets.
    """

    @miru.button(
        label="Groups",
        style=hikari.ButtonStyle.SUCCESS,
        custom_id="support-groups",
    )
    async def groups(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        await self.ephemeral_view(ctx, Groups())

    @miru.button(
        label="Name Changes",
        style=hikari.ButtonStyle.SUCCESS,
        custom_id="support-names",
    )
    async def names(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        await self.ephemeral_view(ctx, Names())

    @miru.button(
        label="Patreon",
        style=hikari.ButtonStyle.SUCCESS,
        custom_id="support-patreon",
    )
    async def patreon(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.patreon(), button)

    @miru.button(
        label="API Key",
        style=hikari.ButtonStyle.SUCCESS,
        custom_id="support-api-key",
    )
    async def api_key(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.api_key(), button)

    @miru.button(
        label="Other",
        style=hikari.ButtonStyle.SUCCESS,
        custom_id="support-other",
    )
    async def other(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        embeds = Injector.get(EmbedService)
        await self.closable_ticket(ctx, embeds.other(), button)


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
