"""
第二步：拉取一个标的的持仓、历史K线数据，为后面交给 Claude 分析做准备。
（模拟账户在非交易时段可能没有实时行情权限，用历史数据 reqHistoricalData 更稳。）
"""

from ib_async import IB, Stock, util

from config import IB_HOST, IB_PORT, IB_CLIENT_ID

SYMBOL = "AAPL"


def main() -> None:
    ib = IB()
    ib.connect(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID, timeout=10)

    contract = Stock(SYMBOL, "SMART", "USD")
    ib.qualifyContracts(contract)

    print(f"正在拉取 {SYMBOL} 最近 30 天的日K线...")
    bars = ib.reqHistoricalData(
        contract,
        endDateTime="",
        durationStr="30 D",
        barSizeSetting="1 day",
        whatToShow="TRADES",
        useRTH=True,
    )

    df = util.df(bars)
    print(df.tail())

    df.to_csv("market_data.csv", index=False)
    print("\n已保存到 market_data.csv")

    positions = ib.positions()
    print("\n当前持仓:")
    for p in positions:
        print(f"  {p.contract.symbol}: {p.position} 股, 均价 {p.avgCost}")

    ib.disconnect()


if __name__ == "__main__":
    main()
