import os

from hom.client import Client


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        # Faster drop in replacement for the asyncio event loop
        # Only works on unix-like systems
        uvloop.install()

    Client.run()
