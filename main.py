import asyncio
from shared_client import start_client
import importlib
import os
import sys

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def main():
    try:
        await load_and_run_plugins()
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        print("Shutting down gracefully...")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        print("Starting clients ...")
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        loop.run_until_complete(asyncio.sleep(1))  # Ensures all tasks finish
        loop.close()
