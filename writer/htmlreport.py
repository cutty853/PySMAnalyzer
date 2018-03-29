#!/usr/bin/python
# coding: utf-8

"""
  Module to write a report in html
"""

from lxml.html import builder
from lxml import etree

BULMA_LINK = "https://cdnjs.cloudflare.com/ajax/libs/bulma/"
BULMA_CSS_LINK = BULMA_LINK + "0.6.2/css/bulma.min.css"

BAD_FILES_SECTION_PATH = ".//body/div[@class='badFiles']"
BAD_FUNCTIONS_SECTION_PATH = ".//body/div[@class='badFunctions']"
BAD_FUNCTION_SECTION_PATH = BAD_FUNCTIONS_SECTION_PATH + "/div[@class='{0}']"

BASIC_FILE_FMT = "<p>- {0} has bad metrics</p>"
BASIC_FILE_SECTION_FMT = "<div class='{0}'><h3>{0}</h3></div>"
BASIC_FUNCTION_FMT = "<p>- {0} has bad metrics</p>"


class HTMLReporter:
    """ The html reporter is able to write the analyzer's report in html """
    def __init__(self):
        self.html_tree = None

    def convert(self):
        """ convert the html report to bytes string """
        return etree.tostring(self.html_tree, pretty_print=True)


    def basic_tree(self):
        """ Create a basic tree for the html report """
        self.html_tree = builder.HTML(
            builder.HEAD(
                builder.TITLE("PySMAnalyzer Report")
            ),
            builder.BODY(
                builder.H1("PySMAnalyzer Report"),
                builder.DIV(
                    builder.CLASS("badFiles"),
                    builder.H2("Bad files")
                ),
                builder.DIV(
                    builder.CLASS("badFunctions"),
                    builder.H2("Bad functions per file")
                )
            )
        )

    def link_css(self):
        """ add a css sttylesheet to the html document """
        self.html_tree.find(".//head").append(etree.HTML(
            "<link rel='stylesheet' href='" + BULMA_CSS_LINK + "' />"
        ))

    def add_file(self, filename):
        """ add a bad file into bad files section into the html tree"""
        bad_files_tree = self.html_tree.find(BAD_FILES_SECTION_PATH)
        bad_files_tree.append(etree.XML(BASIC_FILE_FMT.format(filename)))

    def add_file_section(self, section_name):
        """ add a section to the bad files section """
        bad_functions_tree = self.html_tree.find(BAD_FUNCTIONS_SECTION_PATH)
        bad_functions_tree.append(etree.XML(
            BASIC_FILE_SECTION_FMT.format(section_name)
        ))

    def add_function(self, file_section_name, funcname):
        """ add a bad function in its file section into the html tree """
        bad_function_tree = self.html_tree.find(
            BAD_FUNCTION_SECTION_PATH.format(file_section_name)
        )
        bad_function_tree.append(etree.XML(
            BASIC_FUNCTION_FMT.format(funcname)
        ))
