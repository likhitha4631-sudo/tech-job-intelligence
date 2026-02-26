import csv


def load_job_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    except FileNotFoundError:
        print("ERROR: CSV file not found.")
        return []

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return []
