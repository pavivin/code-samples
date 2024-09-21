import asyncio
from abc import ABC, abstractmethod
from typing import Optional

import aiohttp

from src.exceptions import IPBannedException, RateLimitExceededException


class ResponseHandler(ABC):
    def __init__(self, next_handler: Optional["ResponseHandler"] = None):
        self.next_handler = next_handler

    @abstractmethod
    async def handle(self, response: aiohttp.ClientResponse, symbol: str) -> Optional[str]:
        if self.next_handler:
            return await self.next_handler.handle(response, symbol)
        return None


class Handle429(ResponseHandler):
    async def handle(self, response: aiohttp.ClientResponse, symbol: str) -> Optional[str]:
        if response.status == 429:
            retry_after = int(response.headers.get("Retry-After", 0))
            print(f"Rate limit exceeded for {symbol}. Retrying after {retry_after} seconds...")
            await asyncio.sleep(retry_after)
            raise RateLimitExceededException(f"Rate limit exceeded for {symbol}")
        return await super().handle(response, symbol)


class Handle418(ResponseHandler):
    async def handle(self, response: aiohttp.ClientResponse, symbol: str) -> Optional[str]:
        if response.status == 418:
            retry_after = int(response.headers.get("Retry-After", 60))
            print(f"IP banned for {symbol}. Retrying after {retry_after} seconds...")
            await asyncio.sleep(retry_after)
            raise IPBannedException(f"IP banned for {symbol}")
        return await super().handle(response, symbol)


class Handle400(ResponseHandler):
    async def handle(self, response: aiohttp.ClientResponse, symbol: str) -> Optional[str]:
        if response.status == 400:
            print(f"Bad request for {symbol}. No retries will be attempted.")
            return None  # Прерываем цепочку и возвращаем None без повторных попыток
        return await super().handle(response, symbol)


class DefaultHandler(ResponseHandler):
    async def handle(self, response, symbol: str) -> Optional[str]:
        print(f"Error fetching data for {symbol}: {response.status}")
        return None


binance_handler_chain = Handle418(Handle400(Handle429(DefaultHandler())))
