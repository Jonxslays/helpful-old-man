import arc
import hikari

from hom import Config
from hom import Context
from hom import Hom


async def mods_only(ctx: Context[Hom]) -> arc.HookResult:
    assert ctx.member  # Safe because dm commands are disabled.

    if Config.MOD_ROLE in ctx.member.role_ids:
        return arc.HookResult()

    await ctx.respond(
        "You are not allowed to do that.",
        flags=hikari.MessageFlag.EPHEMERAL,
    )

    return arc.HookResult(abort=True)


@arc.loader
def load(hom: Hom) -> None:
    hom.add_hook(mods_only)
