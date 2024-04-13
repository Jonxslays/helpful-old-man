import logging
from pathlib import Path

import arc

# from hom import Context
from hom import Client
from hom import Plugin

plugin: Plugin[Client] = arc.GatewayPluginBase("support")
logger = logging.getLogger(__name__)


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
    template_count = 0

    for path in Path("hom/data/templates").glob("[!_]*.md"):
        if path.is_dir():
            continue

        name = path.stem.replace("-", "").lower()
        client.add_support_message(name, path.read_text().strip())
        logger.debug(f"Loaded {path.stem} template")
        template_count += 1

    logger.info(f"Loaded {template_count} support message templates!")
    client.add_plugin(plugin)
