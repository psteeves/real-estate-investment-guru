import argparse
from project_real_estate.db import pull_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", required=True, help="Table name to pull.")
    parser.add_argument(
        "-o", "--output-file", required=True, help="File to output data to."
    )
    args = parser.parse_args()

    pull_data(args.table, args.output_file, max_rows=None)


if __name__ == "__main__":
    main()
