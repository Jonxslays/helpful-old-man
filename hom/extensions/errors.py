import logging

import arc
import hikari

from hom import Client
from hom import Embeds
from hom import Plugin

plugin: Plugin[Client] = arc.GatewayPluginBase("errors")
logger = logging.getLogger(__name__)


@plugin.listen()
async def error_handler(event: arc.CommandErrorEvent[Client]) -> None:
    """A function used for handling errors.

    Args:
        event: The command error event that triggered the error.

    Raises:
        The error if it was an unexpected and it should be logged.
    """
    ctx = event.context
    exc = event.exception
    ephemeral = False
    unhandled = False
    message = None

    if isinstance(exc, (arc.UnderCooldownError, arc.MaxConcurrencyReachedError)):
        message = "Someone just used this command, wait a couple seconds."
        ephemeral = True

    elif isinstance(exc, arc.AutocompleteError):
        message = "Failed to calculate autocomplete."
        details = f"{ctx.command.name!r} ({exc.args}) - {exc}"
        logger.error(f"Unable to calculate autocomplete for {details}")

    else:
        # Base case - unexpected error
        message = "An unhandled exception occurred during the command, check the logs."
        unhandled = True

    await Embeds.send_error(ctx, message, ephemeral)

    if unhandled:
        # Re-raise for logging
        raise event.exception


async def interaction_handler(interaction: hikari.ComponentInteraction) -> None:
    await interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        Embeds.info("This button is no longer active."),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@arc.loader
def load(client: Client) -> None:
    client.add_plugin(plugin)
    client.views.set_unhandled_component_interaction_hook(interaction_handler)
