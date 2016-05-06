#!/usr/bin/python
# -*- coding: utf8 -*-
"""Module for simple reading operations."""
import json
import codecs


def read(path, encoding='utf-8'):
    """Retrieve the content of a file."""
    data = None
    with codecs.open(path, 'r', encoding) as f:
        data = f.read()

    return data.replace('\r', '')

def read_json(path, encoding='utf-8'):
    """Retrieve the content of a json file."""
    data = read(path, encoding)
    return json.loads(data)
