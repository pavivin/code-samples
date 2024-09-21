import asyncio
from src.broker import rabbit


async def main():
    await rabbit.startup()
    try:
        async for message in rabbit.listen():
            print(f"Processing message: {message}")
    except Exception as e:
        print(f"Worker error: {e}")
    finally:
        await rabbit.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
