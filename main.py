import json
from pathlib import Path

from src.reader import read_dataset, save_to_file
from src.data_processor import DataProcessor
from src.strategies.console_strategy import ConsoleStrategy
from src.strategies.kafka_strategy import KafkaStrategy
from src.strategies.redis_strategy import RedisStrategy

CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_strategy(config: dict):
    name = config["output_strategy"]
    if name == "console":
        return ConsoleStrategy()
    if name == "kafka":
        kafka_cfg = config["kafka"]
        return KafkaStrategy(
            bootstrap_servers=kafka_cfg["bootstrap_servers"],
            topic=kafka_cfg["topic"],
        )
    if name == "redis":
        redis_cfg = config["redis"]
        return RedisStrategy(
            host=redis_cfg["host"],
            port=redis_cfg["port"],
            key_prefix=redis_cfg["key_prefix"],
        )
    raise ValueError(f"Unknown output_strategy: '{name}'")


def main() -> None:
    config = load_config()

    records = read_dataset(limit=100)
    save_to_file(records)

    strategy = build_strategy(config)
    processor = DataProcessor(strategy)
    processor.process(records)


if __name__ == "__main__":
    main()
