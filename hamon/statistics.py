import argparse
import csv
import unittest
from unittest.mock import patch

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate statistics on unemployment rates.")
    parser.add_argument("--country", required=True, help="Country to perform operation for")
    parser.add_argument("-o", choices=["min", "max", "avg"], default="avg", help="Operation to perform on dates. (Default avg)")
    parser.add_argument("--from", dest="start_year", type=int, help="Starting year (inclusive)")
    parser.add_argument("--to", dest="end_year", type=int, help="Ending year (inclusive)")

    return parser.parse_args()

def filter_data(data, country, start_year=None, end_year=None):
    filtered_data = []

    for entry in data:
        year = int(entry[2])
        if entry[0] == country and (start_year is None or year >= start_year) and (end_year is None or year <= end_year):
            filtered_data.append(entry)

    return filtered_data


def calculate_statistics(data, operation):
    if not data:
        return None

    values = [float(entry[3]) for entry in data]

    if operation == "min":
        return min(values)
    elif operation == "max":
        return max(values)
    elif operation == "avg":
        return sum(values) / len(values)

def main():
    args = parse_args()

    with open("unemployment-rate.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        data = [row for row in reader]

    filtered_data = filter_data(data, args.country, args.start_year, args.end_year)
    result = calculate_statistics(filtered_data, args.o)

    if result is not None:
        print(result)
    else:
        print(f"No data found for {args.country} in the specified date range.")

class TestStatisticsFunctions(unittest.TestCase):
    def setUp(self):
        self.data = [
            ["Belgium", "BEL", 2010, 8.29],
            ["Belgium", "BEL", 2015, 6.78],
            ["Germany", "GER", 2010, 5.12],
            ["Germany", "GER", 2015, 4.76],
        ]

    def test_filter_data(self):
        result = filter_data(self.data, "Belgium", 2010, 2015)
        self.assertEqual(result, [["Belgium", "BEL", 2010, 8.29], ["Belgium", "BEL", 2015, 6.78]])

    def test_calculate_statistics_min(self):
        result = calculate_statistics(self.data, "min")
        self.assertEqual(result, 4.76)

    def test_calculate_statistics_max(self):
        result = calculate_statistics(self.data, "max")
        self.assertEqual(result, 8.29)

    def test_calculate_statistics_avg(self):
        result = calculate_statistics(self.data, "avg")
        self.assertEqual(result, (8.29 + 6.78 + 5.12 + 4.76) / 4)

if __name__ == "__main__":
    main()
    unittest.main()




# commands to run
# python statistics.py --country Germany --from 2010 --to 2012 -o avg
# for unit test
# python statistics.py -m unittest
