import arc

# from hom import Context
from hom import Client
from hom import Plugin

plugin: Plugin = arc.GatewayPluginBase("names")


# @plugin.include
# @arc.slash_command("error", "Force an error")
# async def error_command_func(
#     ctx: Context[Client],
#     recoverable: arc.Option[bool, arc.BoolParams("Is the error recoverable?")] = True,
# ) -> None:
#     print("Running error command")

#     if recoverable:
#         raise RuntimeError("I'm an error!")
#     else:
#         raise Exception("I'm a fatal error!")


@arc.loader
def load(client: Client) -> None:
    client.add_plugin(plugin)
