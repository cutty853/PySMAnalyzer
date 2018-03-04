# coding: utf-8

"""
  Test module for the entity.files module
"""

import unittest
from lxml import etree
import reader.rules_reader as rules_reader


class TestRulesReader(unittest.TestCase):
    """ TestCase for all the functions in the reader.rules_reader module """

    def shortDescription(self):
        return None

    def test_file_abs_path(self):
        """ Test for the file_abs_path """
        self.assertEqual(
            rules_reader.file_abs_path("my_file.c"),
            "/rules/specific/files/file[@name='my_file.c']"
        )

    def test_function_abs_path(self):
        """ Test for the function_abs_path """
        self.assertEqual(
            rules_reader.function_abs_path("my_file.c", "my_func"),
            "/rules/specific/files/file[@name='my_file.c']" +
            "/function_metrics/function[@name='my_func']"
        )

    def test_default_rules_tree(self):
        """ Test for the default_[function|file]_rules_tree, both tested """
        # for the file path finder
        default_file_path = rules_reader.default_file_rules_tree()
        self.assertIsInstance(default_file_path, etree.XPath)
        self.assertEqual(
            str(default_file_path),
            "/rules/default/files/metrics"
        )

        # for the function path finder
        default_function_path = rules_reader.default_function_rules_tree()
        self.assertIsInstance(default_function_path, etree.XPath)
        self.assertEqual(
            str(default_function_path),
            "/rules/default/files/function_metrics"
        )

    def test_specific_rules_tree(self):
        """ Test fort the specific_[file|function]_rules_tree, both tested """
        # specific file path finder
        specific_file_path = rules_reader.specific_file_rules_tree("source.c")
        self.assertIsInstance(specific_file_path, etree.XPath)
        self.assertEqual(
            str(specific_file_path),
            "/rules/specific/files/file[@name='source.c']"
        )

        # specific function path finder
        specific_function_path = rules_reader.specific_function_rules_tree(
            "source.c", "func"
        )
        self.assertIsInstance(specific_function_path, etree.XPath)
        self.assertEqual(
            str(specific_function_path),
            "/rules/specific/files/file[@name='source.c']" +
            "/function_metrics/function[@name='func']"
        )
