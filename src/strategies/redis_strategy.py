import json

from src.strategies.output_strategy import OutputStrategy


class RedisStrategy(OutputStrategy):
    def __init__(self, host: str, port: int, key_prefix: str) -> None:
        try:
            import redis
            self._client = redis.Redis(host=host, port=port, decode_responses=True)
            self._client.ping()
            self._key_prefix = key_prefix
            print(f"[Redis] Connected to {host}:{port}, key prefix: '{key_prefix}'")
        except ImportError:
            raise RuntimeError(
                "redis is not installed. Run: pip install redis"
            )
        except Exception as exc:
            raise RuntimeError(f"[Redis] Connection failed: {exc}") from exc

    def output(self, records: list[dict]) -> None:
        print(f"[Redis] Storing {len(records)} records")
        for record in records:
            key = f"{self._key_prefix}{record['CaseID']}"
            self._client.set(key, json.dumps(record))
        print(f"[Redis] Done. {len(records)} keys stored.")
