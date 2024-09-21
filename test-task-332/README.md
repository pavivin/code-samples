# Test Task 332

Calculate volatility for last 1 hour for few symbols:

BTCUSDT
ETHBTC
LTCBTC
ABOBABTC
DGBBTC
DOGEBTC

Formula:
volatility = (max_high - min_low) / min_low * 100

Data source:
https://api.binance.com/api/v3/klines?Docs for method:
https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=60


Код написан на Python 3.11

1. Установить зависимости

```bash
pip install -r requirements.txt
```

2. Запустить

```bash
python main.py
```

3. Радоваться

```bash
;)
```