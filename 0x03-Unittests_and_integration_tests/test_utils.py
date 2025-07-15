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

    @parameterized.expand([
        # Test case 1: Simple, top-level key
        ({"a": 1}, ("a",), 1),
        
        # Test case 2: Path to a nested dictionary
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        
        # Test case 3: Path to a value inside a nested dictionary
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Tests that `access_nested_map` correctly returns the value at the
        end of a given path in a nested dictionary.
        
        Args:
            nested_map (dict): The dictionary to access.
            path (tuple): A tuple representing the path of keys.
            expected_result: The value expected to be returned by the function.
        """
        # This is the first line of the test method's body
        actual_result = access_nested_map(nested_map, path)
        
        # This is the second line, fulfilling the "not longer than 2 lines" requirement
        self.assertEqual(actual_result, expected_result)