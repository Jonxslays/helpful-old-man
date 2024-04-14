import hikari
import miru

__all__ = ("TicketBase",)


class TicketBase(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(label="Close", custom_id="support-ticket-close", style=hikari.ButtonStyle.SUCCESS)
    async def groups(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        print("Ticket channel has been closed?????")
