import asyncio
from asyncio import Semaphore

import aiohttp

from src.exceptions import IPBannedException, RateLimitExceededException
from src.response_handler import binance_handler_chain
from src.schemas import BinanceCandle


class CandleRequestHandler:
    default_headers = {"accept": "application/json"}
    default_timeout = 5

    max_retries = 3

    @classmethod
    async def _fetch_json(cls, session: aiohttp.ClientSession, semaphore: Semaphore, url: str, params: dict):
        retry_count = 0
        while retry_count < cls.max_retries:
            async with semaphore:
                try:
                    async with session.get(
                        url, params=params, headers=cls.default_headers, timeout=cls.default_timeout
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data

                        result = await binance_handler_chain.handle(response, params.get("symbol", ""))
                        if result is None:
                            return None
                        retry_count += 1
                        continue

                except (aiohttp.ClientError, RateLimitExceededException, IPBannedException) as e:
                    print(f"Request error: {e}")
                    retry_count += 1
                    await asyncio.sleep(1)

        print("Max retries exceeded.")
        return None

    @classmethod
    async def fetch_candles(cls, session: aiohttp.ClientSession, semaphore: Semaphore, symbol: str):
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": "1m", "limit": 60}
        raw_candles = await cls._fetch_json(session, semaphore, url, params)
        if not isinstance(raw_candles, list):
            print(f"Caught error while fetching candles: {symbol} {raw_candles}, {raw_candles.__class__.__name__}")
            return
        candles = [BinanceCandle(*raw_candle) for raw_candle in raw_candles]
        return candles
