#!/usr/bin/python
# -*- coding: utf8 -*-
"""Manage different data formats: (csv, xls, json)."""
import reader
import writer
import pandas
import enum
import filepath

Format = enum.Enum('Format', 'csv json xls xlsx')


def transform(in_path, out_format):
    """Transform a given file from one format to another."""
    ext = filepath.get_extension(in_path)[1:]
    in_format = None

    for f in Format.__members__:
        if ext == f:
            in_format = Format[f]
            break

    out_path = in_path.replace(in_format.name, out_format.name)
    read_write(in_path, in_format, out_path, out_format)


def read_write(in_path, in_format, out_path, out_format):
    """Read a file and write it in another format."""
    dataframe = read(in_path, in_format)
    write(out_path, dataframe, out_format)


def read(path, in_format):
    """Read a dataframe from a given path with a given format."""
    dataframe = None
    if in_format == Format.csv:
        dataframe = pandas.read_csv(path)
    elif in_format == Format.json:
        json_object = reader.read_json(path)
        dataframe = pandas.DataFrame.from_dict(json_object)
    elif in_format in {Format.xls, Format.xlsx}:
        dataframe = pandas.read_excel(path)

    return dataframe

def write(path, dataframe, out_format):
    """Write the dataframe to a given path with a given format."""
    if out_format == Format.csv:
        dataframe.to_csv(path, index=False)
    elif out_format == Format.json:
        dataframe.to_json(path, orient='split', force_ascii=False)
    elif out_format in {Format.xls, Format.xlsx}:
        dataframe.to_excel(path, index=False)

def unit_test():
    """Test the module."""
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    unit_test()

    transform(
        '/home/ariel/Downloads/data.csv', Format.xls
    )