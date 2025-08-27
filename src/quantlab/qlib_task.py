import pandas as pd, akshare as ak
from pathlib import Path
from quantlab.config import settings


def etl():
    """下载沪深300日线并转成 Qlib 格式"""
    Path("data/qlib").mkdir(exist_ok=True, parents=True)
    # 简单示例：只拿前 10 只
    symbols = ak.index_stock_cons_sina("hs300")["代码"].tolist()[:10]
    symbols = [s + ".SH" if s.startswith("6") else s + ".SZ" for s in symbols]
    all_df = []
    for s in symbols:
        df = ak.stock_zh_a_hist(symbol=s[:6], period="daily", start_date="20230101")
        if not df.empty:
            df["symbol"] = s
            df["date"] = pd.to_datetime(df["日期"])
            df = df[["date", "symbol", "开盘", "收盘", "最高", "最低", "成交量"]]
            df.columns = [
                "date",
                "instrument",
                "$open",
                "$close",
                "$high",
                "$low",
                "$volume",
            ]
            all_df.append(df)
    raw = pd.concat(all_df)
    raw.to_csv("data/qlib/features.csv", index=False)
    import os

    os.system(
        "python -m qlib.contrib.data.dump_bin --csv_path data/qlib --qlib_dir data/qlib"
    )


def train():
    """极简 LightGBM 训练示例"""
    import qlib
    from qlib.config import REG_CN
    from qlib.contrib.data.handler import Alpha158
    from qlib.contrib.model.gbdt import LGBModel

    qlib.init(provider_uri="data/qlib", region=REG_CN)
    hd = Alpha158(
        start_time="2023-01-01",
        end_time="2024-12-31",
        fit_start_time="2023-01-01",
        fit_end_time="2023-12-31",
        instruments="csi300",
    )
    model = LGBModel()
    model.fit(hd)
    pred = model.predict(hd)
    pred.to_pickle("output/pred.pkl")


if __name__ == "__main__":
    import fire

    fire.Fire({"etl": etl, "train": train})
