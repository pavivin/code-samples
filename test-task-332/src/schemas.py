from typing import NamedTuple


class BinanceCandle(NamedTuple):
    open_time: int
    open_price: str
    high: str
    low: str
    close: str
    volume: str
    close_time: int
    quote_asset_volume: str
    number_of_trades: int
    taker_buy_base_asset_volume: str
    taker_buy_quote_asset_volume: str
    ignore: str
