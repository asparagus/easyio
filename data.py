#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Manage different data formats and their operations.

Permitted formats: csv, json, xls, xlsx.
"""
import reader
import pandas
import enum
import filepath
import random

Format = enum.Enum('Format', 'csv json xls xlsx')


def transform(in_path, out_format):
    """Transform a given file from one format to another."""
    in_format = infer_format(in_path)
    out_path = in_path.replace(in_format.name, out_format.name)

    data = read(in_path, in_format)
    write(out_path, data, out_format)


def infer_format(path):
    """Infer the format of the data using the file extension."""
    ext = filepath.get_extension(path)
    if not ext:
        raise ValueError(
            "The input file has no extension, cannot infer a format.")

    format_name = ext[1:]
    if format_name in Format.__members__:
        return Format[format_name]
    else:
        raise ValueError(
            "The file's extension (" +
            format_name +
            ")does not correspond to a valid format.")


def read(path, in_format=None, encoding='utf-8', csv_delimiter=','):
    """Read a dataframe from a given path with a given format."""
    if not in_format:
        in_format = infer_format(path)

    dataframe = None
    if in_format == Format.csv:
        dataframe = pandas.read_csv(
            path, delimiter=csv_delimiter, encoding=encoding)
    elif in_format == Format.json:
        json_object = reader.read_json(path, encoding=encoding)
        dataframe = pandas.DataFrame.from_dict(json_object)
    elif in_format in {Format.xls, Format.xlsx}:
        dataframe = pandas.read_excel(path, encoding=encoding)
    else:
        raise ValueError("Invalid file extension %s" % in_format)

    return dataframe


def write(
        path, dataframe, out_format=None, encoding='utf-8', csv_delimiter=','):
    """Write the dataframe to a given path with a given format."""
    if not out_format:
        out_format = infer_format(path)

    filepath.create_path(path)
    if out_format == Format.csv:
        dataframe.to_csv(
            path, index=False, delimiter=csv_delimiter, encoding=encoding)
    elif out_format == Format.json:
        dataframe.to_json(
            path, orient='split', force_ascii=False, encoding=encoding)
    elif out_format in {Format.xls, Format.xlsx}:
        dataframe.to_excel(path, index=False, encoding=encoding)
    else:
        raise ValueError("Invalid file extension %s" % out_format)


def concat(files, out_path):
    """Concatenate multiple files."""
    dataframes = [read(path) for path in files]
    concat_dataframe = pandas.concat(dataframes, ignore_index=True)
    write(out_path, concat_dataframe)


def split(dataframe, fractions):
    """Split a dataframe according to the given fractions."""
    if not fractions:
        raise ValueError("Need fractions for the split.")

    if len(fractions) == 1:
        return [dataframe]

    s = sum(fractions)
    x, xs = fractions[0], fractions[1:]
    first, rest = binary_split(dataframe, 1.0 * x / s)

    return [first] + split(rest, xs)


def binary_split(dataframe, fraction):
    """Split a dataframe in two according to the given fraction."""
    n = dataframe.shape[0]
    all_indices = dataframe.index.values

    first_n = int(n * fraction)
    first_indices = random.sample(all_indices, first_n)

    set_first_indices = set(first_indices)
    second_indices = [i for i in all_indices if i not in set_first_indices]

    first_data = dataframe.loc[first_indices, :]
    second_data = dataframe.loc[second_indices, :]
    return first_data, second_data


def unit_test():
    """Test the module."""
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    unit_test()
    files = filepath.get_files(
        '../sensus-algorithm/output/sentiment/v13/csv', '.csv')

    for f in files:
        transform(f, Format.xls)

    # files = filepath.get_files(
    #     '../sensus-algorithm/output/sentiment/v13/xls')

    # concat(files, '../sensus-algorithm/output/sentiment/v13/xls/full.xlsx')
