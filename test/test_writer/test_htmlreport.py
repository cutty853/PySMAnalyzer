#!/usr/bin/python
# coding: utf-8

"""
  test module for the htmlreport writer
"""

import unittest
from lxml import etree
import writer.htmlreport as htmlreport


CONVERTION_RESULT = """<html>
  <head>
    <title>PySMAnalyzer Report</title>
    <link rel="stylesheet" href="{}"/>
  </head>
  <body>
    <h1>PySMAnalyzer Report</h1>
    <div class="badFiles">
      <h2>Bad files</h2>
      <p>- banane.c has bad metrics</p>
    </div>
    <div class="badFunctions">
      <h2>Bad functions per file</h2>
      <div class="banane.c">
        <h3>banane.c</h3>
        <p>- my_func has bad metrics</p>
      </div>
    </div>
  </body>
</html>
""".format(htmlreport.BULMA_CSS_LINK)


class TestHTMLReport(unittest.TestCase):
    """ TestCase for the html report writer """

    def shortDescription(self):
        return None

    def setUp(self):
        self.html_reporter = htmlreport.HTMLReporter()
        self.html_reporter.basic_tree()

    def tearDown(self):
        del self.html_reporter

    def test_convert(self):
        """ test for the convert methods """
        self.html_reporter.link_css()
        self.html_reporter.add_file_section("banane.c")
        self.html_reporter.add_file("banane.c")
        self.html_reporter.add_function("banane.c", "my_func")

        self.assertEqual(
            self.html_reporter.convert().decode(),
            CONVERTION_RESULT
        )

    def test_basic_tree(self):
        """ test for the basic_tree methods """
        # Just test if the basic tree is what it should be
        self.assertEqual(
            etree.tostring(self.html_reporter.html_tree),
            b"<html><head><title>PySMAnalyzer Report</title></head><body>"
            b"<h1>PySMAnalyzer Report</h1>"
            b"<div class=\"badFiles\"><h2>Bad files</h2></div>"
            b"<div class=\"badFunctions\"><h2>Bad functions per file</h2></div>"
            b"</body></html>"
        )

    def test_link_css(self):
        """ test for the link_css methods """
        self.html_reporter.link_css()

        # Testing if the link tag has been added (present and correct)
        link = self.html_reporter.html_tree.find(".//head/link")
        self.assertIsNotNone(link)
        self.assertEqual(
            etree.tostring(link),
            '<link rel="stylesheet" href="{}"/>'.format(
                htmlreport.BULMA_CSS_LINK
            ).encode("utf-8")
        )

    def test_add_file(self):
        """ test for the add_file methods """
        self.html_reporter.add_file("banane.c")
        new_bad_file = self.html_reporter.html_tree.find(
            ".//body/div[@class='badFiles']"
        )[1]

        # Is the new info on the bad file present
        self.assertIsNotNone(new_bad_file)
        self.assertEqual(
            etree.tostring(new_bad_file),
            b'<p>- banane.c has bad metrics</p>'
        )

    def test_add_file_section(self):
        """ test for the add_file_section methods """
        self.html_reporter.add_file_section("banane.c")

        # Getting the new file section tree
        new_section = self.html_reporter.html_tree.find(
            ".//body/div[@class='badFunctions']/div[@class='banane.c']"
        )

        # Is the new section present and correct
        self.assertIsNotNone(new_section)
        self.assertEqual(
            etree.tostring(new_section),
            b'<div class="banane.c"><h3>banane.c</h3></div>'
        )

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
            ".//body/div[@class='badFunctions']/div[@class='banane.c']"
        )[1]

        # Testing if it's present and correct
        self.assertIsNotNone(new_function)
        self.assertEqual(
            etree.tostring(new_function),
            b'<p>- my_func has bad metrics</p>'
        )
