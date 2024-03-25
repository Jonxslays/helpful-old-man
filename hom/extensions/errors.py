import arc
import hikari

from hom import Hom


async def error_handler(event: arc.CommandErrorEvent[Hom]) -> None:
    if isinstance(event.exception, (arc.UnderCooldownError, arc.MaxConcurrencyReachedError)):
        await event.context.respond(
            "Someone just used this command, wait a couple seconds.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

        return None

    # Base case - unexpected error
    await event.context.respond(
        "An unhandled exception occurred during the command, check the logs."
    )

    # Re-raise for logging
    raise event.exception


@arc.loader
def load(hom: Hom) -> None:
    hom.subscribe(arc.CommandErrorEvent, error_handler)
