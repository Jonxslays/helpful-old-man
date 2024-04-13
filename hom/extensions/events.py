import arc

from hom import Client
from hom import Context
from hom import Plugin

plugin: Plugin[Client] = arc.GatewayPluginBase("events")


@plugin.include
@arc.slash_command("err", "Force an error for testing")
async def error_command_func(
    ctx: Context[Client],
) -> None:
    print("Running error command")
    raise RuntimeError("I'm an error!")


@arc.loader
def load(client: Client) -> None:
    client.add_plugin(plugin)
