#!/usr/bin/python
# coding: utf-8

"""
  Module to write a report in html
"""

from lxml.html import builder
from lxml import etree

BULMA_LINK = "https://cdnjs.cloudflare.com/ajax/libs/bulma/"
BULMA_CSS_LINK = BULMA_LINK + "0.6.2/css/bulma.min.css"

BAD_FILES_SECTION_PATH = ".//body/div/div/div/div[@id='badFiles']/table/tbody"
BAD_FUNCTIONS_SECTION_PATH = ".//body/div/div/div/div[@id='badFunctions']"
BAD_FUNCTION_SECTION_PATH = BAD_FUNCTIONS_SECTION_PATH + "/div[@class='{0}']/table/tbody"

TABLE_HTML = """
<table class='table'>
    <thead>
        <tr>
            <th>Function name</th>
            <th>Problem's description</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>
"""
BASIC_FILE_FMT = "<tr><td>{0}</td><td>has bad metrics</td></tr>"
BASIC_FILE_SECTION_FMT = "<div class='{0}'><h3 class='title has-text-primary'>{0}</h3>" + TABLE_HTML + "</div>"
BASIC_FUNCTION_FMT = "<tr><td>{0}</td><td>has bad metrics</td></tr>"

LOGO_PATH = "images/terminal.svg"


class NoSection(IndexError):
    """ raised when no section file was found for a function """
    pass


class HTMLReporter:
    """ The html reporter is able to write the analyzer's report in html """
    def __init__(self):
        self.html_tree = None

    def load_layout(self):
        """ Load the existing html layout """
        html_parser = etree.HTMLParser(remove_comments=True)
        self.html_tree = etree.parse("html/layout.html", parser=html_parser)

    def convert(self):
        """ convert the html report to bytes string """
        return etree.tostring(self.html_tree, pretty_print=True, method='html')

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
        if bad_function_tree is None:
            raise NoSection("There is no file section for this function")

        bad_function_tree.append(etree.XML(
            BASIC_FUNCTION_FMT.format(funcname)
        ))