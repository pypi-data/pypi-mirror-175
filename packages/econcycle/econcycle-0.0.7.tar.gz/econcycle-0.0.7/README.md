# econcycle

This package is to define economic cycle for a given timeframe. (Inflation, Recession, Goldilocks)

It also gives trend information of the stock.

## Installation

Install package

```sh
pip install econcycle
```

## Getting Started

```python
from econcycle.utils.cycle import Cycle
from econcycle.utils.chart import Chart

start_date = "2020-01-01 00:00:00"
end_date = "2022-11-08 00:00:00"

resolution = "W"

# This period is used to calculate trend of candle data.
# If it is uptrend, the chart is going up,
# If it is downtrend, the chart is going down
period = 5

# Get all cycles (Inlfation, Recession, Goldilocks)
cycle = Cycle(resolution, period, start_date, end_date)
all_cycle = cycle.get_all()

print(all_cycle)

# Get chart data of AAPL
aapl = chart.process("AAPL")
print(aapl)

# Get trend information (uptrend, downtrend)
print(aapl.get("type"))

```

## License

MIT
