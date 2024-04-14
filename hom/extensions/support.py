import logging
from pathlib import Path

import arc
import hikari

from hom import Context
from hom import Client
from hom import Embeds
from hom import Plugin
from hom import Replacer
from hom import views

plugin: Plugin[Client] = arc.GatewayPluginBase("support")
logger = logging.getLogger(__name__)


support = plugin.include_slash_group("support", "Support related commands.")


@support.include
@arc.slash_subcommand("send", "Send the support embed to a channel.")
async def support_send(
    ctx: Context[Client],
    channel: arc.Option[
        hikari.GuildTextChannel, arc.ChannelParams("The channel to send the embed to.")
    ],
) -> None:
    view = views.Support()
    embed = Embeds.support(
        ctx.client,
        "Need help from one of our moderators?",
        Replacer.replace_support_template(ctx.client),
    )

    response = await ctx.client.create_message(channel, embed, components=view)
    ctx.client.start_view(view, bind_to=response)
    await ctx.respond(Embeds.success("Support embed has been sent."))


@arc.loader
def load(client: Client) -> None:
    template_count = 0

    for path in Path("hom/data/templates").glob("[!_]*.md"):
        if path.is_dir():
            continue

        name = path.stem.replace("-", "").lower()
        client.add_support_template(name, path.read_text().strip())
        logger.debug(f"Loaded {path.stem} template")
        template_count += 1

    logger.info(f"Loaded {template_count} support message templates!")
    client.add_plugin(plugin)
