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

INFOS_BOX = ".//body/div[@id='entityInfos']"
BAD_FILES_INFO_BOX = INFOS_BOX + "div/div/div[@id='files']"
BAD_FUNCTIONS_INFO_BOX = INFOS_BOX + "div/div/div[@id='functions']"
WORST_FILE_INFO_BOX = INFOS_BOX + "div/div/div[@id='worst_file']"

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
BASIC_BAD_FILES_INFOBOX_FMT = "<p>There are {0} bad files</p>"
BASIC_BAD_FUNCTIONS_INFOBOX_FMT = "<p>There are {0} bad functions !</p>"
BASIC_WORST_FILE_INFOBOX_FMT = "<p>The file with the most bad functions is {0}</p>"

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

    def change_bad_files_amount(self, new_amount):
        """ change the amount of bad files in the html tree """
        bad_files_infobox = self.html_tree.find(BAD_FILES_INFO_BOX)
        bad_files_infobox.append(etree.XML(BASIC_BAD_FILES_INFOBOX_FMT.format(new_amount)))

    def change_bad_functions_amount(self, new_amount):
        """ change the amount of bad functions in the html tree """
        bad_func_infobox = self.html_tree.find(BAD_FUNCTIONS_INFO_BOX)
        bad_func_infobox.append(etree.XML(BASIC_BAD_FUNCTIONS_INFOBOX_FMT.format(new_amount)))

    def change_worst_file_name(self, new_name):
        """ change the name of the worst file in the html tree """
        worst_file_infobox = self.html_tree.find(WORST_FILE_INFO_BOX)
        worst_file_infobox.append(etree.XML(BASIC_WORST_FILE_INFOBOX_FMT.format(new_name)))

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
