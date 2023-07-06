import csv, os
from .record import Record


class DB:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

        if not os.path.exists(filepath):
            self.__create_csv_file()

    def __create_csv_file(self):
        with open(self.filepath, mode="w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=Record.HEADERS)
            writer.writeheader()
            writer.writerows([])

    def add_record(self, record: Record):
        with open(self.filepath, mode="a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=Record.HEADERS)
            writer.writerow(
                {
                    "date": record.date,
                    "score": record.score,
                    "kills": record.kills,
                    "coins": record.coins,
                }
            )

    def is_there_any_higher_records(self, record: Record):
        with open(self.filepath, mode="r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                if int(row["score"]) > record.score:
                    return True

        return False

    def clear_all_records(self):
        self.__create_csv_file()

    def get_all_records(self):
        records = []

        with open(self.file_path, mode="r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                records.append(
                    Record(
                        coins=int(row["coins"]),
                        date=row["date"],
                        kills=int(row["kills"]),
                        score=int(row["score"]),
                    )
                )

        return records
