import backtrader as bt, pandas as pd, pickle
from pathlib import Path


class TopkStrategy(bt.Strategy):
    params = dict(topk=5)

    def __init__(self):
        self.signal = pd.read_pickle("output/pred.pkl").unstack("instrument")["score"]

    def next(self):
        today = self.datas[0].datetime.date(0)
        if today not in self.signal.index:
            return
        sig = self.signal.loc[today]
        topk = sig.nlargest(self.p.topk)
        for d in self.datas:
            if d._name in topk.index:
                self.order_target_percent(d, 1.0 / self.p.topk)
            else:
                self.order_target_percent(d, 0)


def main():
    cerebro = bt.Cerebro()
    # 示例：用 akshare 拿 000001 日线
    import akshare as ak

    df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101")
    df["trade_date"] = pd.to_datetime(df["日期"])
    df.set_index("trade_date", inplace=True)
    df = df[["开盘", "最高", "最低", "收盘", "成交量"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    data = bt.feeds.PandasData(dataname=df, name="000001.SZ")
    cerebro.adddata(data)
    cerebro.addstrategy(TopkStrategy)
    cerebro.broker.setcash(100_000)
    cerebro.run()
    # 简化为持仓变化写 csv
    orders = [
        {"date": "2024-06-28", "symbol": "000001.SZ", "action": "BUY", "size": 1000}
    ]
    pd.DataFrame(orders).to_csv("output/orders.csv", index=False)


if __name__ == "__main__":
    main()
