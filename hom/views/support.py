import hikari
import miru

__all__ = ("Support",)


class Support(miru.View):
    def __init__(self) -> None:
        self._click_count = 0
        super().__init__()

    @miru.button(label="Increment", style=hikari.ButtonStyle.PRIMARY)
    async def increment(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        self._click_count += 1
        await ctx.message.edit(f"The click count is {self._click_count}", components=self)

    @miru.button(label="Cancel", style=hikari.ButtonStyle.SECONDARY)
    async def cancel(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        await ctx.message.edit(f"The final count was {self._click_count}", components=[])
        self.stop()
