import csv


class Commons:
    def __init__(self) -> None:
        pass

    def read_javascript(self, file_path):
        with open(file_path, "r") as file:
            return file.read()

    def read_csv_data(self, file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return {row["Name"]: row["Value"] for row in reader}

    def alt_field_map(self, input_dir):
        alt_field_map = {}
        with open(input_dir, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    if value:  # Only add non-empty alternatives
                        alt_field_map[value.lower()] = key
        return alt_field_map
