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

    df.sort_values(by=["ChannelNo", "StartTime"], inplace=True)

    df_list = df.values.tolist()

    for index in range(len(df_list)):
        if df_list[index][7] == "C":
            # Previous programme
            if index > 0 and df_list[index][1] == df_list[index - 1][1] and df_list[index - 1][7] == "P":
                end_time = datetime.datetime.strptime(str(df_list[index - 1][2]), "%Y%m%d%H%M%S") + datetime.timedelta(seconds=df_list[index - 1][3])
                if df_list[index - 1][2] <= df_list[index][2]:
                    df_list[index].append(df_list[index - 1][0])
        
        if len(df_list[index]) < 9:
            df_list[index].append("N/A")

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
        csv_writer.writerow(["ContentIndicator", "ID", "ChannelNo", "Starttime", "Duration", "Title", "Genre", "Owner", "LinkedId"])
        for data in content:
            csv_writer.writerow([data[7], data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[8]])

if __name__ == "__main__":
    main()
