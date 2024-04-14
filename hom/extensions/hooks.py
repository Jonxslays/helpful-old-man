import functools
import logging

import arc

from hom import Client
from hom import Config
from hom import Context
from hom import EmbedService

logger = logging.getLogger(__name__)


async def mods_only(embeds: EmbedService, ctx: Context) -> arc.HookResult:
    """Limits command invocations to mods only.

    Args:
        ctx (`Context[Client]`): The command context.

    Returns:
        `HookResult`: The result of the hook, either success
            or failure.
    """
    assert ctx.member  # Safe because dm commands are disabled.

    if Config.MOD_ROLE in ctx.member.role_ids:
        return arc.HookResult()

    user = f"{ctx.member.username} ({ctx.member.id})"
    logger.debug(f"Permission denied for {user} executing command {ctx.command.name!r}")
    await embeds.send_error(ctx, "You are not allowed to do that.", ephemeral=True)
    return arc.HookResult(abort=True)


@arc.loader
def load(client: Client) -> None:
    embeds = client.get_type_dependency(EmbedService)
    hook = functools.partial(mods_only, embeds)
    client.add_hook(hook)
