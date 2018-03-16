# coding: utf-8

"""
  Test module for the entity.files module
"""

import unittest
from lxml import etree

import reader.rules_reader as rules_reader
import entity.files as files


class TestFile(unittest.TestCase):
    """ Test case for the File class in the entity.files module """
    def shortDescription(self):
        return None

    def setUp(self):
        xml_parser = etree.XMLParser(remove_comments=True)
        self.tree = etree.parse("samples/sample.xml", parser=xml_parser)
        self.rules_tree = etree.parse(
            "samples/rules_sample.xml", parser=xml_parser
        )
        self.test_file = files.File(r"STV\Trieuse\stv\src\ttpdsext.c")

    def tearDown(self):
        del self.tree
        del self.rules_tree
        del self.test_file

    def test___str__(self):
        """ test string conversion """
        final_string =  \
            r"File called STV\Trieuse\stv\src\ttpdsext.c has 0 functions"
        metrics_final_string = final_string + \
            " has following metrics:\n" + \
            "  M0: 461\n" + "  M1: 289\n" + "  M2: 24.6\n" + "  M3: 16.3\n" + \
            "  M4: 6\n" + "  M5: 42.7\n" + "  M6: 88\n" + \
            "  M7: progexplttpdsext()\n" + "  M8: 78\n" + "  M9: 328\n" + \
            "  M10: 9+\n" + "  M11: 5.51\n" + "  M12: 17.0"

        # Basic string output (without metrics)
        self.assertEqual(str(self.test_file), final_string)

        # Complex string ouput (with metrics)
        self.test_file.load_metrics(self.tree)
        self.assertEqual(str(self.test_file), metrics_final_string)

    def test_search_file_tree(self):
        """
            Test for the search_tree method used to search a specific
            function's tree
        """
        my_bad_file = files.File(r"STV\Trieuse\stv\src\kldslkd.c")
        with self.assertRaises(files.FileNotFound):
            my_bad_file.search_file_tree(self.tree)

        # We can't test all the equality on the tree (too big)
        # So we test that it seems to be a source-monitor file tree
        file_tree = self.test_file.search_file_tree(self.tree)
        self.assertEqual(len(file_tree), 3)
        self.assertEqual(file_tree[0].tag, "metrics")
        self.assertEqual(file_tree[1].tag, "function_metrics")
        self.assertEqual(file_tree[2].tag, "block_depths")

    def test_load_metrics(self):
        """ test the load_metrics method """
        # The asked file doesn't exist in the sample file
        my_bad_file = files.File(r"STV\Trieuse\stv\src\ttdsext.c")
        with self.assertRaises(files.FileNotFound):
            my_bad_file.load_metrics(self.tree)

        self.test_file.load_metrics(self.tree)
        self.assertEqual(self.test_file.metrics.get("M0"), 461)
        self.assertEqual(self.test_file.metrics.get("M1"), 289)
        self.assertEqual(self.test_file.metrics.get("M2"), 24.6)
        self.assertEqual(self.test_file.metrics.get("M3"), 16.3)
        self.assertEqual(self.test_file.metrics.get("M4"), 6)
        self.assertEqual(self.test_file.metrics.get("M5"), 42.7)
        self.assertEqual(self.test_file.metrics.get("M6"), 88)
        self.assertEqual(
            self.test_file.metrics.get("M7"), "progexplttpdsext()"
        )
        self.assertEqual(self.test_file.metrics.get("M8"), 78)
        self.assertEqual(self.test_file.metrics.get("M9"), 328)
        self.assertEqual(self.test_file.metrics.get("M10"), "9+")
        self.assertEqual(self.test_file.metrics.get("M11"), 5.51)
        self.assertEqual(self.test_file.metrics.get("M12"), 17.0)

    def test_load_functions(self):
        """ test for the load_functions method """
        self.test_file.load_functions(self.tree)

        # All functions are here
        self.assertNotEqual(self.test_file.functions, None)
        self.assertEqual(len(self.test_file.functions), 6)
        for function in self.test_file.functions:
            self.assertIn(function.name, {
                "initttpdsext()", "majtabpdsext()", "progexplttpdsext()",
                "proginterttpdsext()", "razttpdsext()", "recuppdsext()"
            })
            self.assertNotEqual(function.metrics, None)  # metrics are loaded

        # a file with no function doesn't have 'function_metrics' block in the
        # source-monitor report ...
        header_file = files.File(r"STV\Trieuse\stv\src\ttpdsext.h")
        header_file.load_functions(self.tree)
        self.assertEqual(len(header_file.functions), 0)

    def test_load_default_rules(self):
        """ test for the load_default_rules method """
        with self.assertRaises(rules_reader.BadRulesFormat):
            self.test_file.load_default_rules(self.tree)

        self.test_file.load_default_rules(self.rules_tree)
        self.assertNotEqual(self.test_file.rules, None)
        self.assertDictEqual(
            self.test_file.rules._metrics,  # pylint: disable=protected-access
            {
                "M0": 0, "M1": 0, "M2": 0, "M3": 0, "M4": 0,
                "M5": 0, "M6": 0, "M7": "disable", "M8": 0, "M9": 0,
                "M10": 0, "M11": 0, "M12": 0
            }
        )

    def test_load_specific_rules(self):
        """ test for the load_specific_rules method """
        with self.assertRaises(rules_reader.BadRulesFormat):
            self.test_file.load_specific_rules(self.tree)

        no_rules_files = files.File(r"STV\Trieuse\stv\src\vcscope.c")
        no_rules_files.load_specific_rules(self.rules_tree)
        # Rules did not change from default rules
        self.assertDictEqual(
            no_rules_files.rules._metrics,  # pylint: disable=protected-access
            {
                "M0": 0, "M1": 0, "M2": 0, "M3": 0, "M4": 0,
                "M5": 0, "M6": 0, "M7": "disable", "M8": 0, "M9": 0,
                "M10": 0, "M11": 0, "M12": 0
            }
        )

        # specific rules
        self.test_file.load_specific_rules(self.rules_tree)
        self.assertDictEqual(
            self.test_file.rules._metrics,  # pylint: disable=protected-access
            {
                "M0": "disable", "M1": "disable", "M2": "disable",
                "M3": 1, "M4": "disable", "M5": "disable",
                "M6": "disable", "M7": "disable", "M8": "disable",
                "M9": "disable", "M10": "disable", "M11": "disable",
                "M12": "disable"
            }
        )

    def test_load_rules(self):
        """ Test for the load_rules method """
        self.test_file.load_rules(self.rules_tree)

        # it load something
        self.assertNotEqual(self.test_file.rules, None)

    def test_check_validity(self):
        """ Test for the check validity method """
        self.test_file.load_metrics(self.tree)
        self.test_file.load_rules(self.rules_tree)
        self.test_file.check_validity()

        # With this rules the file is not ok
        self.assertFalse(self.test_file.validity)

    def test_load(self):
        """ test for the load method """
        self.test_file.load(self.tree, self.rules_tree)

        # testing if it has done something
        # more tests: test_load_metrics, test_load_metrics, test_check_validity
        self.assertNotEqual(self.test_file.rules, None)
        self.assertNotEqual(self.test_file.metrics, None)
        self.assertNotEqual(len(self.test_file.functions), 0)
