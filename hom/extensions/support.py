import arc

# from hom import Context
from hom import Hom
from hom import Plugin

plugin: Plugin[Hom] = arc.GatewayPluginBase("support")


# @plugin.include
# @arc.slash_command("error", "Force an error")
# async def error_command_func(
#     ctx: Context[Hom],
#     recoverable: arc.Option[bool, arc.BoolParams("Is the error recoverable?")] = True,
# ) -> None:
#     print("Running error command")

#     if recoverable:
#         raise RuntimeError("I'm an error!")
#     else:
#         raise Exception("I'm a fatal error!")


@arc.loader
def load(hom: Hom) -> None:
    hom.add_plugin(plugin)
