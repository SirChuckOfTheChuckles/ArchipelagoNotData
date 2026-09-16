"""
Unit tests for custom mission orders
"""

import unittest
from ..mission_order import index_parsing
from Options import OptionError


class TestIndexParsing(unittest.TestCase):
    def test_basic_arithmetic(self) -> None:
        term = "1 + 2*3 - 4/2"
        tokens = index_parsing.tokenize(term)
        result = index_parsing.parse_int_expression(term, tokens, {}, (), 0, "testing")
        self.assertEqual(result, 5)

    def test_parentheses(self) -> None:
        term = "(1+2) * (3 - 1)"
        tokens = index_parsing.tokenize(term)
        result = index_parsing.parse_int_expression(term, tokens, {}, (), 0, "testing")
        self.assertEqual(result, 6)

    def test_unary_minus(self) -> None:
        term = "-1 + (-1 - +3)"
        num_missions = 10
        tokens = index_parsing.tokenize(term)
        result = index_parsing.parse_int_expression(term, tokens, {}, (), num_missions, "testing")
        self.assertEqual(result, -5 + num_missions)

    def test_unclosed_parenthesis_errors(self) -> None:
        term = "(1+2) * (3 - 1"
        tokens = index_parsing.tokenize(term)
        try:
            result = index_parsing.parse_int_expression(term, tokens, {}, (), 0, "testing")
            self.fail("Expected an exception")
        except OptionError as ex:
            self.assertIn("offset 8", str(ex))

    def test_doubled_operators_errors(self) -> None:
        term = "3 + * 3"
        tokens = index_parsing.tokenize(term)
        try:
            result = index_parsing.parse_int_expression(term, tokens, {}, (), 0, "testing")
            self.fail("Expected an exception")
        except OptionError as ex:
            self.assertIn("offset 4", str(ex))
