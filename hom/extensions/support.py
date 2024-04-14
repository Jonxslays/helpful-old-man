import logging

import arc
import hikari

from hom import Context
from hom import Client
from hom import Plugin
from hom import TemplateSection
from hom import EmbedService
from hom import TemplateService
from hom import views

plugin: Plugin = arc.GatewayPluginBase("support")
support = plugin.include_slash_group("support", "Support related commands.")
logger = logging.getLogger(__name__)


@support.include
@arc.slash_subcommand("send", "Send the support embed to a channel.")
async def support_send(
    ctx: Context,
    channel: arc.Option[
        hikari.GuildTextChannel, arc.ChannelParams("The channel to send the embed to.")
    ],
    embeds: EmbedService = arc.inject(),
    templates: TemplateService = arc.inject(),
) -> None:
    raise Exception("DFDKDKDKD")
    body = templates.get_support_template()
    footer = templates.get_template(TemplateSection.Reminder)
    embed = embeds.support(body, footer)

    await ctx.client.create_message(channel, embed, components=views.Support())
    await ctx.respond(embeds.success("Support embed has been sent."))

    logger.debug(f"Mod {ctx.author} ({ctx.author.id}) sent the support embed to #{channel}")


@arc.loader
def load(client: Client) -> None:
    client.add_plugin(plugin)
