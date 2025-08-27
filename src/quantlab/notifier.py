import os, requests, csv
from quantlab.config import settings


def push(file="output/orders.csv"):
    if not os.path.exists(file):
        return
    with open(file) as f:
        rows = list(csv.DictReader(f))
    msg = "今日交易信号：\n" + "\n".join(
        [f"{r['symbol']} {r['action']} {r['size']}" for r in rows]
    )
    if settings.feishu_webhook:
        requests.post(
            settings.feishu_webhook, json={"msg_type": "text", "content": {"text": msg}}
        )
