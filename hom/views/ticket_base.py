import hikari
import miru

__all__ = ("TicketBase",)


class TicketBase(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(
        label="Close",
        emoji="\N{LOCK}",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="support-ticket-close",
    )
    async def close_ticket(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        print(f"Ticket channel {ctx.get_channel()} would close now... if it could.")
