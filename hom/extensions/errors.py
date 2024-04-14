import functools
import logging
import secrets

import arc
import hikari

from hom import Client
from hom import EmbedService

logger = logging.getLogger(__name__)


async def error_handler(embeds: EmbedService, event: arc.CommandErrorEvent[Client]) -> None:
    """A function used for handling errors.

    Args:
        event: The command error event that triggered the error.

    Raises:
        The error if it was an unexpected and it should be logged.
    """
    reference = secrets.token_hex(12)
    ctx = event.context
    exc = event.exception
    ephemeral = False
    unhandled = False
    message = None

    if isinstance(exc, (arc.UnderCooldownError, arc.MaxConcurrencyReachedError)):
        message = "Someone just used this command, wait a couple seconds."
        reference = None
        ephemeral = True

    elif isinstance(exc, arc.AutocompleteError):
        unhandled = True
        message = "Exception while calculating autocomplete."

    else:
        unhandled = True
        message = "An unhandled exception occurred during the command, check the logs."

    footer = f"Reference: {reference}" if reference else None
    await embeds.send_error(ctx, message, ephemeral=ephemeral, footer=footer)

    if unhandled:
        # Re-raise for logging
        logger.error(f"Exception reference: {reference}")
        raise event.exception


async def interaction_handler(
    embeds: EmbedService, interaction: hikari.ComponentInteraction
) -> None:
    await interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        embeds.info("This button is no longer active."),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@arc.loader
def load(client: Client) -> None:
    embeds = client.get_type_dependency(EmbedService)

    inter_handler = functools.partial(interaction_handler, embeds)
    err_handler = functools.partial(error_handler, embeds)

    client.views.set_unhandled_component_interaction_hook(inter_handler)
    client.subscribe(arc.CommandErrorEvent, err_handler)
