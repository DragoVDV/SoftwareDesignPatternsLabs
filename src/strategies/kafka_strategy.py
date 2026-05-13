import json

from src.strategies.output_strategy import OutputStrategy


class KafkaStrategy(OutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        try:
            from kafka import KafkaProducer
            self._producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            self._topic = topic
            print(f"[Kafka] Connected to {bootstrap_servers}, topic: {topic}")
        except ImportError:
            raise RuntimeError(
                "kafka-python is not installed. Run: pip install kafka-python"
            )
        except Exception as exc:
            raise RuntimeError(f"[Kafka] Connection failed: {exc}") from exc

    def output(self, records: list[dict]) -> None:
        print(f"[Kafka] Sending {len(records)} records to topic '{self._topic}'")
        for record in records:
            self._producer.send(self._topic, value=record)
        self._producer.flush()
        print(f"[Kafka] Done. {len(records)} records sent.")
