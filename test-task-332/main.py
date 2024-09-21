import asyncio

import aiohttp

from src.calculator import VolatilityCalculator
from src.candle_api import CandleRequestHandler

listing = (
    "BTCUSDT",
    "ETHBTC",
    "LTCBTC",
    "ABOBABTC",
    "DGBBTC",
    "DOGEBTC",
)


async def main():
    semaphore = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        tasks = [
            CandleRequestHandler.fetch_candles(session=session, symbol=symbol, semaphore=semaphore)
            for symbol in listing
        ]
        results = await asyncio.gather(*tasks)
        if not results:
            return

        for symbol, candles in zip(listing, results):
            volatility = VolatilityCalculator().calculate(candles)
            print(f"{symbol}: Volatility = {volatility:.2f}%")


if __name__ == "__main__":
    asyncio.run(main())
