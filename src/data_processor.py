from src.strategies.output_strategy import OutputStrategy


class DataProcessor:
    def __init__(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def process(self, records: list[dict]) -> None:
        self._strategy.output(records)
