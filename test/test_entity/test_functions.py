# coding: utf-8

"""
  Test module for the entity.functions module
"""

import unittest
from lxml import etree

import reader.rules_reader as rules_reader
import entity.functions as functions


class TestFunction(unittest.TestCase):
    """ Test case for the Function class in the entity.functions module """
    def shortDescription(self):
        return None

    def setUp(self):
        xml_parser = etree.XMLParser(remove_comments=True)
        self.tree = etree.parse("samples/sample.xml", parser=xml_parser)
        self.rules_tree = etree.parse(
            "samples/rules_sample.xml", parser=xml_parser
        )
        self.test_func = functions.Function(
            r"STV\Trieuse\stv\src\ttpdsext.c", "initttpdsext()"
        )

    def tearDown(self):
        del self.tree
        del self.test_func

    def test___str__(self):
        """ string conversion test """
        final_string =  \
            r"Function called initttpdsext() in STV\Trieuse\stv\src\ttpdsext.c"
        metrics_final_string = final_string + \
            " has following metrics:\n" + \
            "  complexity: 6\n" + "  statements: 25\n" + \
            "  maximum_depth: 4\n" + "  calls: 0"

        # Basic string output (without metrics)
        self.assertEqual(str(self.test_func), final_string)

        # Complex string ouput (with metrics)
        self.test_func.load_metrics(self.tree)
        self.assertEqual(str(self.test_func), metrics_final_string)

    def test_search_tree(self):
        """
            Test for the search_tree method used to search a specific
            function's tree
        """
        my_bad_func = functions.Function(
            r"STV\Trieuse\stv\src\ttpdsext.c", "test()"
        )
        with self.assertRaises(functions.FunctionNotFound):
            my_bad_func.search_tree(self.tree)

        self.assertEqual(
            etree.tostring(self.test_func.search_tree(self.tree)),
            b'<function name="initttpdsext()" line="35">\n' +
            b'                <complexity>6</complexity>\n' +
            b'                <statements>25</statements>\n' +
            b'                <maximum_depth>4</maximum_depth>\n' +
            b'                <calls>0</calls>\n' +
            b'              </function>\n              '
        )

    def test_load_metrics(self):
        """ test the load_metrics method """
        # The asked function doesn't exist in the sample file
        my_bad_func = functions.Function(
            r"STV\Trieuse\stv\src\ttpdsext.c", "initttpxt()"
        )

        with self.assertRaises(functions.FunctionNotFound):
            my_bad_func.load_metrics(self.tree)

        self.test_func.load_metrics(self.tree)
        self.assertEqual(self.test_func.metrics.complexity, 6)
        self.assertEqual(self.test_func.metrics.statements, 25)
        self.assertEqual(self.test_func.metrics.maximum_depth, 4)
        self.assertEqual(self.test_func.metrics.calls, 0)

    def test_load_default_rules(self):
        """ Test for the load_default_rules method of the Function class """
        # testing with a file which is not a xml rules file
        with self.assertRaises(rules_reader.BadRulesFormat):
            self.test_func.load_default_rules(self.tree)

        self.test_func.load_default_rules(self.rules_tree)
        self.assertEqual(self.test_func.rules.complexity, 10)
        self.assertEqual(self.test_func.rules.statements, "disable")
        self.assertEqual(self.test_func.rules.maximum_depth, "disable")
        self.assertEqual(self.test_func.rules.calls, "disable")

    def test_load_specific_rules(self):
        """ Test for the load_specific_rules method of the Function class """
        with self.assertRaises(rules_reader.BadRulesFormat):
            self.test_func.load_default_rules(self.tree)

        # function that has no specific rules
        no_rules_func = functions.Function(
            r"STV\Trieuse\stv\src\ttpdsext.c", "majtabpdsext()"
        )
        no_rules_func.load_specific_rules(self.rules_tree)
        self.assertEqual(no_rules_func.rules.complexity, 10)
        self.assertEqual(no_rules_func.rules.statements, "disable")
        self.assertEqual(no_rules_func.rules.maximum_depth, "disable")
        self.assertEqual(no_rules_func.rules.calls, "disable")

        # We don't pre-load the default rules, load_specific_rules will do it
        self.test_func.load_specific_rules(self.rules_tree)
        self.assertEqual(self.test_func.rules.complexity, 5)
        self.assertEqual(self.test_func.rules.statements, "disable")
        self.assertEqual(self.test_func.rules.maximum_depth, "disable")
        self.assertEqual(self.test_func.rules.calls, "disable")

    def test_load_rules(self):
        """
            Test the load_rules method, only verify if function load something
        """
        self.test_func.load_rules(self.rules_tree)
        self.assertNotEqual(self.test_func.rules, None)

    def test_check_validity(self):
        """
            Test the check_validity method which say if some function's metrics
            are ok according to rules
        """
        self.test_func.load_metrics(self.tree)
        self.test_func.load_rules(self.rules_tree)

        self.test_func.check_validity()
        self.assertFalse(self.test_func.validity)
