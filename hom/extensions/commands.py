import logging

import arc
import hikari

from hom import Client
from hom import Context
from hom import EmbedService
from hom import Injector
from hom import Plugin
from hom import views

plugin: Plugin = arc.GatewayPluginBase("commands")
support = plugin.include_slash_group("support", "Support related commands.")
logger = logging.getLogger(__name__)


@support.include
@arc.slash_subcommand("send", "Send the support embed to a channel.")
async def support_send(
    ctx: Context,
    /,
    channel: arc.Option[  # type: ignore[valid-type]
        hikari.GuildTextChannel,
        arc.ChannelParams("The channel to send the embed to."),
    ],
) -> None:
    embeds = Injector.get(EmbedService)
    embed = embeds.support()
    flags = hikari.MessageFlag.EPHEMERAL

    message = await ctx.client.create_message(channel, embed, components=views.Support())
    jump_link = message.make_link(ctx.guild_id)

    await ctx.respond(embeds.success(f"Success! {jump_link}."), flags=flags)
    logger.debug(f"Mod {ctx.author} ({ctx.author.id}) sent the support embed to #{channel}")


@arc.loader
def load(client: Client) -> None:
    client.add_plugin(plugin)
