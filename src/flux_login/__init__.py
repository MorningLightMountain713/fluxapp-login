import asyncio

from flux_login.manager import FluxAppManager


def run():
    async def main():
        app = FluxAppManager()
        await app.login()

    asyncio.run(main())


if __name__ == "__main__":
    run()
