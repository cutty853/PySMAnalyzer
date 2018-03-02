# coding: utf-8

"""
  Test module for the entity.files module
"""

import unittest
from lxml import etree

import entity.files as files


class TestFile(unittest.TestCase):
    """ Test case for the File class in the entity.files module """
    def shortDescription(self):
        return None

    def test___str__(self):
        """ test string conversion """
        my_file = files.File(r"STV\Trieuse\stv\src\ttpdsext.c")
        final_string =  \
            r"File called STV\Trieuse\stv\src\ttpdsext.c has 0 functions"
        metrics_final_string = final_string + \
            " has following metrics:\n" + \
            "  M0: 461\n" + "  M1: 289\n" + "  M2: 24.6\n" + "  M3: 16.3\n" + \
            "  M4: 6\n" + "  M5: 42.7\n" + "  M6: 88\n" + \
            "  M7: progexplttpdsext()\n" + "  M8: 78\n" + "  M9: 328\n" + \
            "  M10: 9+\n" + "  M11: 5.51\n" + "  M12: 17.0"

        # Basic string output (without metrics)
        self.assertEqual(str(my_file), final_string)

        # Complex string ouput (with metrics)
        tree = etree.parse("samples/sample.xml")
        my_file.load_metrics(tree)
        self.assertEqual(str(my_file), metrics_final_string)

    def test_load_metrics(self):
        """ test the load_metrics method """
        tree = etree.parse("samples/sample.xml")
        my_file = files.File(r"STV\Trieuse\stv\src\ttpdsext.c")
        # The asked file doesn't exist in the sample file
        my_bad_file = files.File(r"STV\Trieuse\stv\src\ttdsext.c")

        with self.assertRaises(files.FileNotFound):
            my_bad_file.load_metrics(tree)

        my_file.load_metrics(tree)
        self.assertEqual(my_file.metrics.get("M0"), 461)
        self.assertEqual(my_file.metrics.get("M1"), 289)
        self.assertEqual(my_file.metrics.get("M2"), 24.6)
        self.assertEqual(my_file.metrics.get("M3"), 16.3)
        self.assertEqual(my_file.metrics.get("M4"), 6)
        self.assertEqual(my_file.metrics.get("M5"), 42.7)
        self.assertEqual(my_file.metrics.get("M6"), 88)
        self.assertEqual(my_file.metrics.get("M7"), "progexplttpdsext()")
        self.assertEqual(my_file.metrics.get("M8"), 78)
        self.assertEqual(my_file.metrics.get("M9"), 328)
        self.assertEqual(my_file.metrics.get("M10"), "9+")
        self.assertEqual(my_file.metrics.get("M11"), 5.51)
        self.assertEqual(my_file.metrics.get("M12"), 17.0)
