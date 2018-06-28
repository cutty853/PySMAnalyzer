# coding: utf-8

"""
  Test module for the entity.metrics module
"""

import unittest
import entity.reports as reports
import entity.functions as functions
import entity.files as files


class TestReport(unittest.TestCase):
    """docstring for TestReport """
    def shortDescription(self):
        return None

    def setUp(self):
        self.test_report = reports.Report()
        # declaring all files
        self.test_files = set(
            [files.File("test_file.c"), files.File("second.c")]
        )
        for file_ in self.test_files:
            file_.validity = False
        # declaring all functions
        self.functions = {
            "test_file.c": functions.Function("test_file.c", "func"),
            "second.c": functions.Function("second.c", "second")
        }
        self.functions["test_file.c"].validity = False
        self.functions["second.c"].validity = False
        # adding one function to each file
        for file_ in self.test_files:
            file_.functions.add(self.functions[file_.name])

    def tearDown(self):
        del self.test_report

    def test_new_bad_functions(self):
        """ test the new_bad_functions method """
        report = self.test_report
        report.new_bad_functions("test_file.c")

        self.assertSetEqual(report.bad_functions["test_file.c"], set())
        self.assertEqual(report.nb_bad_functions, 0)

    def test_add_bad_function(self):
        """ test the add_bad_function """
        second_test_func = functions.Function("test_file.c", "second")
        report = self.test_report

        report.add_bad_function(self.functions["test_file.c"])
        self.assertEqual(report.nb_bad_functions, 1)
        self.assertEqual(report.nb_bad_functions_for_file["test_file.c"], 1)
        self.assertEqual(len(report.bad_functions), 1)
        self.assertEqual(len(report.bad_functions["test_file.c"]), 1)

        report.add_bad_function(second_test_func)
        self.assertEqual(report.nb_bad_functions, 2)
        self.assertEqual(report.nb_bad_functions_for_file["test_file.c"], 2)
        self.assertEqual(len(report.bad_functions), 1)
        self.assertEqual(len(report.bad_functions["test_file.c"]), 2)

    def test_load_bad_functions(self):
        """ test for the load_bad_functions method """
        report = self.test_report

        report.load_bad_functions(self.test_files)
        # It fill a dict with set for each file
        self.assertSetEqual(
            report.bad_functions["test_file.c"],
            set([self.functions["test_file.c"]])
        )
        self.assertSetEqual(
            report.bad_functions["second.c"],
            set([self.functions["second.c"]])
        )
        # It also count functions
        self.assertEqual(report.nb_bad_functions, 2)
        self.assertEqual(report.nb_bad_functions_for_file["test_file.c"], 1)
        self.assertEqual(report.nb_bad_functions_for_file["second.c"], 1)

    def test_load_bad_files(self):
        """ test the load bad files report """
        report = self.test_report

        report.load_bad_files(self.test_files)
        self.assertEqual(report.nb_bad_files, 2)
        self.assertEqual(len(report.bad_files), 2)
        self.assertSetEqual(report.bad_files, self.test_files)

    def test_make_report(self):
        """ test the make_report method """
        report = self.test_report
        report.make_report(self.test_files)

        # Testing that it has made somthing
        # see test_load_bad_files and test_load_bad_functions
        self.assertTrue(report.bad_functions)
        self.assertTrue(report.bad_files)
