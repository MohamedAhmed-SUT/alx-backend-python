#!/usr/bin/env python3
"""
This module contains unit tests for the `utils.access_nested_map` function.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the `access_nested_map` function from `utils.py`.
    """

    # --- Task 0 Code (Already complete and correct) ---
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Tests that `access_nested_map` returns the correct value for valid paths.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # --- Task 1 Code (New method to add) ---
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Tests that `access_nested_map` raises a KeyError for invalid paths.
        """
        # The `assertRaises` context manager checks if a specific exception is raised.
        # The test will fail if the code inside the `with` block does NOT raise a KeyError.
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
        # Optional but good practice: Check that the exception message is correct.
        # It should be the key that was not found.
        # self.assertEqual(str(context.exception), f"'{path[-1]}'")