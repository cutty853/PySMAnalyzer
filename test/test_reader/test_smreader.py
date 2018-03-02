# coding: utf-8

"""
  Test module for the entity.files module
"""

import unittest
from lxml import etree
import reader.smreader as smreader


class TestFinders(unittest.TestCase):
    """ TestCase for all the functions in the reader.smreader module """

    def shortDescription(self):
        return None

    def test_function_abs_path(self):
        """ test for the absolute path function """
        # Only testing function_abs_path is enough because it will call
        # file_abs_path which itself calls last_checkpoint_abs_path
        self.assertEqual(
            smreader.function_abs_path("test_source.c", "my_func"),
            "/sourcemonitor_metrics/project/checkpoints/checkpoint[last()]" +
            "/files/file[@file_name='test_source.c']" +
            "/function_metrics/function[@name='my_func']"
        )

    def test_create_file_finder(self):
        """ test for the function that create XPath file finder """
        file_finder = smreader.create_file_finder("test_source.c")

        self.assertIsInstance(file_finder, etree.XPath)
        self.assertEqual(
            str(file_finder),
            "/sourcemonitor_metrics/project/checkpoints/checkpoint[last()]" +
            "/files/file[@file_name='test_source.c']"
        )

    def test_create_function_finder(self):
        """ test for the function that create XPath function finder """
        func_finder = smreader.create_function_finder(
            "test_source.c", "my_func"
        )

        self.assertIsInstance(func_finder, etree.XPath)
        self.assertEqual(
            str(func_finder),
            "/sourcemonitor_metrics/project/checkpoints/checkpoint[last()]" +
            "/files/file[@file_name='test_source.c']/" +
            "function_metrics/function[@name='my_func']"
        )
