import os

from hom.client import Client

if __name__ == "__main__":
    if os.name != "nt":
        # Faster drop in replacement for the asyncio event loop
        import uvloop  # Not available on windows (lol)

        uvloop.install()

    Client.run()  # Blocks the main thread
