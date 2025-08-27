import argparse, importlib

STEPS = {
    "etl": "qlib_task",
    "train": "qlib_task",
    "backtest": "bt_task",
    "notify": "notifier",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=list(STEPS.keys()) + ["daily"])
    args = parser.parse_args()
    if args.mode == "daily":
        for step in ["etl", "train", "backtest", "notify"]:
            mod = importlib.import_module(f"quantlab.{STEPS[step]}")
            getattr(mod, step if step != "notify" else "push")()
    else:
        mod = importlib.import_module(f"quantlab.{STEPS[args.mode]}")
        getattr(mod, args.mode if args.mode != "notify" else "push")()


if __name__ == "__main__":
    main()
