import arc

from hom import Client

# from hom import Context
from hom import Plugin

# from hom import views

plugin: Plugin[Client] = arc.GatewayPluginBase("events")


# @plugin.include
# @arc.slash_command("basic", "Test the basic view")
# async def error_command_func(
#     ctx: Context[Client],
# ) -> None:
#     view = views.BasicView()
#     await ctx.respond("The click count is 0", components=view)
#     ctx.client.views.start_view(view)


@arc.loader
def load(client: Client) -> None:
    client.add_plugin(plugin)
