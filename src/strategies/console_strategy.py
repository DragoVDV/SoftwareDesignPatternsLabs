from src.strategies.output_strategy import OutputStrategy


class ConsoleStrategy(OutputStrategy):
    def output(self, records: list[dict]) -> None:
        print(f"[Console] Outputting {len(records)} records\n")
        for record in records:
            print(
                f"ID: {record['CaseID']} | "
                f"Opened: {record['Opened']} | "
                f"Category: {record['Category']} | "
                f"Status: {record['Status']} | "
                f"Address: {record['Address']}"
            )
