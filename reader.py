#!/usr/bin/python
# -*- coding: utf8 -*-
"""Module for simple reading operations."""
import json
import codecs
import pickle


def read_text(path, encoding='utf-8'):
    """Retrieve the content of a file."""
    data = None
    with codecs.open(path, 'r', encoding) as f:
        data = f.read()

    return data.replace('\r', '')


def read_json(path, encoding='utf-8'):
    """Retrieve the content of a json file."""
    data = read_text(path, encoding)
    return json.loads(data)


def read_binary(path):
    """Retrieve an object from a binary file."""
    with open(path, 'rb') as f:
        binary_object = pickle.load(f)
    return binary_object
