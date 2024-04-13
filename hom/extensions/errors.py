import arc
import hikari

from hom import Client


async def error_handler(event: arc.CommandErrorEvent[Client]) -> None:
    """A function used for handling errors.

    Args:
        event (`arc.CommandErrorEvent[Client]`): The command error event
            that triggered the error.

    Raises:
        `Exception`: The error if it was an unexpected and it should
            be logged.
    """
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
def load(client: Client) -> None:
    client.subscribe(arc.CommandErrorEvent, error_handler)
