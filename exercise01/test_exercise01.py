#!/usr/bin/env python

import os
import pytest

from exercise01 import process_file

def test_exercise01_process_filei_01():
    actual, expected = process("01")
    assert actual == expected


def test_exercise01_process_filei_02():
    actual, expected = process("02")
    assert actual == expected


def process(test_name):
    input_file = os.path.join("test_case", "test_{}.txt".format(test_name))
    output_file = os.path.join("test_case", "test_{}_result.txt".format(test_name))
    expected_file = os.path.join("test_case", "test_{}.result".format(test_name))

    process_file(input_file, output_file)

    with open(output_file) as text_file:
        actual = text_file.read()
    with open(expected_file) as text_file:
        expected = text_file.read()

    return actual, expected
