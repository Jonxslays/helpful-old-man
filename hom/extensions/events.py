import arc

from hom import Context
from hom import Hom
from hom import Plugin

plugin: Plugin[Hom] = arc.GatewayPluginBase("events")


@plugin.include
@arc.slash_command("err", "Force an error for testing")
async def error_command_func(
    ctx: Context[Hom],
) -> None:
    print("Running error command")
    raise RuntimeError("I'm an error!")


@arc.loader
def load(hom: Hom) -> None:
    hom.add_plugin(plugin)
