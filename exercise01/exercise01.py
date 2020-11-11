#!/usr/bin/env python

import os
import csv
import pandas
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, help='Path to the input file')
    parser.add_argument('--output-file', type=str, help='Path to the output file')
    args = parser.parse_args()

    process_file(args.input_file, args.output_file)


def process_file(input_file, output_file):
    if not is_file_path_valid(input_file):
        print("error=File doesn't exists or it's not a file, file_path=".format(file_path))
        return

    try:
        df = get_file_content(input_file)
    except Exception as e:
        print("error={}".format(repr(e)))
        return

    df.sort_values(by=["HomeNo", "Starttime"], inplace=True)

    df_list = df.values.tolist()

    for index in range(len(df_list)):
        # EndTime
        if index < len(df_list) - 1 and df_list[index][0] == df_list[index + 1][0]:
            temp = datetime.datetime.strptime(str(df_list[index + 1][2]), "%Y%m%d%H%M%S") - datetime.timedelta(seconds=1)
            df_list[index].append(int(temp.strftime("%Y%m%d%H%M%S")))
        else:
            partial = "{}{}".format(str(df_list[index][2])[:8], "240000")
            df_list[index].append(int(partial))

        # Duration
        start_time = str(df_list[index][2])
        if str(df_list[index][4])[8:] == "240000":
            end_time = "{}{}".format(str(df_list[index][4])[:8], "235959")
        else:
            end_time = str(df_list[index][4])
        duration = datetime.datetime.strptime(end_time, "%Y%m%d%H%M%S") - datetime.datetime.strptime(start_time, "%Y%m%d%H%M%S")
        df_list[index].append(duration.seconds + 1)

    try:
        write_output_file(output_file, df_list)
    except Exception as e:
        print("error={}".format(repr(e)))


def is_file_path_valid(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)


def get_file_content(file_path):
    result = pandas.read_csv(file_path, sep="|", header=0)

    return result


def write_output_file(output_file, content):
    with open(output_file, "w") as f:
        csv_writer = csv.writer(f, delimiter="|")
        csv_writer.writerow(["HomeNo", "Channel", "Starttime", "Activity", "EndTime", "Duration"])
        for data in content:
            csv_writer.writerow(data)

if __name__ == "__main__":
    main()
