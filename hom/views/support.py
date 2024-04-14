import hikari
import miru

__all__ = ("Support",)


class Support(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(label="Groups", custom_id="support-groups", style=hikari.ButtonStyle.SUCCESS)
    async def groups(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed GROUPS", components=self)
        print("Clicks groups")

    @miru.button(label="Name Changes", custom_id="support-names", style=hikari.ButtonStyle.SUCCESS)
    async def names(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed NAMES", components=self)
        print("Clicks names")

    @miru.button(label="Patreon", custom_id="support-patreon", style=hikari.ButtonStyle.SUCCESS)
    async def patreon(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed PATREON", components=self)
        print("Clicks patreon")

    @miru.button(label="API Key", custom_id="support-api-key", style=hikari.ButtonStyle.SUCCESS)
    async def api_key(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed API KEY", components=self)
        print("Clicks api key")

    @miru.button(label="Other", custom_id="support-other", style=hikari.ButtonStyle.SUCCESS)
    async def other(self, ctx: miru.ViewContext, _: miru.Button) -> None:
        # await ctx.message.edit(f"You pressed OTHER", components=self)
        print("Clicks other")
