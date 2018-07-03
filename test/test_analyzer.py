#!/usr/bin/python
# coding: utf-8

"""
  MODULE DOCUMENTATION
"""

import unittest
import analyzer


class TestAnalyzer(unittest.TestCase):
    """ TestCase for the Analyzer class """
    def shortDescription(self):
        return None

    def setUp(self):
        self.sm_analyzer = analyzer.Analyzer(
            "samples/sample.xml", "samples/rules_sample.xml"
        )

    def tearDown(self):
        del self.sm_analyzer

    def test_load_files(self):
        """ test the load_files method """
        # tests variables
        filenames = [
            r"STV\Trieuse\stv\src\ttpdsext.c",
            r"STV\Trieuse\stv\src\ttpdsext.h",
            r"STV\Trieuse\stv\src\ttvideo.c",
            r"STV\Trieuse\stv\src\ttvideo.h",
            r"STV\Trieuse\stv\src\vcscope.c",
            r"STV\Trieuse\stv\src\vcscope.h"
        ]
        file_order = {filenames[i]: i for i in range(len(filenames))}

        # call the method
        self.sm_analyzer.load_files()

        # there are 6 functions and their names corresponds to filenames
        self.assertEqual(len(self.sm_analyzer.files), 6)
        for file_, filename in zip(
                sorted(
                    self.sm_analyzer.files, key=lambda x: file_order[x.name]
                ),
                filenames
        ):
            self.assertEqual(file_.name, filename)

        # Not testing all metrics
        # see test_functions.py, test_files.py, test_metrics.py


def create_test_suite():
    """ main du programme """
    return unittest.TestLoader().loadTestsFromTestCase(TestAnalyzer)
