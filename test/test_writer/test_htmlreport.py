#!/usr/bin/python
# coding: utf-8

"""
  test module for the htmlreport writer
"""

import unittest
from lxml import etree
import writer.htmlreport as htmlreport


class TestHTMLReport(unittest.TestCase):
    """ TestCase for the html report writer """

    def shortDescription(self):
        return None

    def setUp(self):
        self.html_reporter = htmlreport.HTMLReporter()
        self.html_reporter.load_layout()

    def tearDown(self):
        del self.html_reporter

    def test_convert(self):
        """ test for the convert methods """
        self.html_reporter.add_file_section("banane.c")
        self.html_reporter.add_file("banane.c")
        self.html_reporter.add_function("banane.c", "my_func")

        with open("test/test_writer/convert_result.html", "r") as expected_result:
            self.assertEqual(
                self.html_reporter.convert().decode(),
                "".join(expected_result.readlines())
            )

    def test_add_file(self):
        """ test for the add_file methods """
        self.html_reporter.add_file("banane.c")
        new_bad_file = self.html_reporter.html_tree.find(
            htmlreport.BAD_FILES_SECTION_PATH
        )[0]

        # Is the new info on the bad file present
        self.assertIsNotNone(new_bad_file)
        # Testing correctness is to tedious
        # self.assertEqual(
        #     etree.tostring(new_bad_file),
        #     b'<tr><td>banane.c</td><td>has bad metrics</td></tr>'
        # )

    def test_add_file_section(self):
        """ test for the add_file_section methods """
        self.html_reporter.add_file_section("banane.c")

        # Getting the new file section tree
        new_section = self.html_reporter.html_tree.find(
            htmlreport.BAD_FUNCTIONS_SECTION_PATH + "/div[@class='banane.c']"
        )

        # Is the new section present
        self.assertIsNotNone(new_section)
        # Testing correctness is to tedious
        # self.assertEqual(
        #     etree.tostring(new_section),
        #     b'<div class="banane.c"><table>banane.c</table></div>'
        # )

    def test_add_function(self):
        """ test for the add_function methods """
        # We must add the section before !
        with self.assertRaises(htmlreport.NoSection):
            self.html_reporter.add_function("banane.c", "my_func")

        # Adding the section and then the function
        self.html_reporter.add_file_section("banane.c")
        self.html_reporter.add_function("banane.c", "my_func")

        # Getting the new function tree
        new_function = self.html_reporter.html_tree.find(
            htmlreport.BAD_FUNCTION_SECTION_PATH.format("banane.c")
        )[0]

        # Testing if it's present
        self.assertIsNotNone(new_function)
        # Testing correctness is to tedious
        # self.assertEqual(
        #     etree.tostring(new_function),
        #     b'<p>- my_func has bad metrics</p>'
        # )
