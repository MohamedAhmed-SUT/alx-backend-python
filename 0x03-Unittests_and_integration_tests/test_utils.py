#!/usr/bin/env python3
"""
This module contains unit tests for the functions in `utils.py`.
It tests `access_nested_map`, `get_json`, and `memoize`.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """A test suite for the `utils.access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Tests that `access_nested_map` returns the expected output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
        """Tests that a KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """A test suite for the `utils.get_json` function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """
        Tests that `get_json` works correctly by mocking HTTP calls.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        with patch('utils.requests.get', return_value=mock_response) as mocked_get:
            result = get_json(test_url)
            mocked_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """A test suite for the `utils.memoize` decorator."""

    def test_memoize(self) -> None:
        """
        Tests that the `memoize` decorator caches the result of a method.
        """
        class TestClass:
            """A test class with a method and a memoized property."""
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mocked_method:
            instance = TestClass()
            
            # Call the property twice
            self.assertEqual(instance.a_property, 42)
            self.assertEqual(instance.a_property, 42)
            
            # Assert that the underlying method was only called once
            mocked_method.assert_called_once()