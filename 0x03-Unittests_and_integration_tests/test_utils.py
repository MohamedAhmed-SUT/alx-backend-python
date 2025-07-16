#!/usr/bin/env python3
"""
This module contains unit tests for the functions in `utils.py`.
It thoroughly tests `access_nested_map` for both valid and invalid cases.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """
    A test suite for the `utils.access_nested_map` function.
    This class tests the function's ability to access values in
    nested dictionaries using a key path.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: Mapping,
                               path: Sequence,
                               expected: Any) -> None:
        """
        Tests that `access_nested_map` returns the expected output
        for a variety of valid nested map structures and paths.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Mapping,
                                         path: Sequence) -> None:
        """
        Tests that a KeyError is raised when `access_nested_map` is
        called with a path that does not exist within the nested map.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # This checks that the exception message is the key that was not found.
        # Although not strictly required by the prompt, it's good practice.
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


# You will add the other test classes (TestGetJson, TestMemoize) below this
# as you complete the next tasks.