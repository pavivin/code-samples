from decimal import Decimal

from src.schemas import BinanceCandle


class VolatilityCalculator:
    def calculate(self, candles: list[BinanceCandle]) -> Decimal:
        if not candles:
            return Decimal("0")

        max_high = Decimal(max(candles, key=lambda x: Decimal(x.high)).high)

        min_low = Decimal(min(candles, key=lambda x: Decimal(x.low)).low)

        volatility = (max_high - min_low) / min_low * Decimal("100")
        return volatility
