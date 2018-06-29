#!/usr/bin/python
# coding: utf-8

"""
  Module to write a report in xml
"""


from lxml import etree


LAYOUT_STRING = """
<psma>
    <global_infos>
        <bad_file_amount></bad_file_amount>
        <bad_function_amount></bad_function_amount>
        <worst_file></worst_file>
    </global_infos>
    <bad_files></bad_files>
    <bad_functions></bad_functions>
</psma>
"""


class SECTIONS_FINDER:
    """ Intern finders to search for sections in the generated xml report """
    # Finders are quite simple since the name of the secions are unique
    BAD_FILES = ".//bad_files"
    BAD_FUNCTIONS = ".//bad_functions"
    BAD_FUNCTIONS_FOR_FILE = ".//bad_functions/file_section[@name='{0}']"
    BAD_FILE_AMOUNT = ".//bad_file_amount"
    BAD_FUNCTION_AMOUNT = ".//bad_function_amount"
    WORST_FILE = ".//worst_file"


class FMT:
    BAD_FILE = "<file>{0}</file>"
    BAD_FUNCTION = "<function>{0}</function>"
    BAD_FUNCTION_FOR_FILE = "<file_section name='{0}'></file_section>"


class NoSection(IndexError):
    """ raised when no section file was found for a function """
    pass


class XMLReporter:
    """ The class that create the xml report """
    def __init__(self):
        self.xmltree = None

    def load_layout(self):
        self.xmltree = etree.fromstring(LAYOUT_STRING)

    def convert(self):
        """ convert the html report to bytes string """
        return etree.tostring(self.xmltree, pretty_print=True)

    def add_file(self, filename):
        """ add a file to the bad files section """
        self.xmltree.find(SECTIONS_FINDER.BAD_FILES).append(
            etree.XML(FMT.BAD_FILE.format(filename))
        )

    def add_file_section(self, filename):
        """ add a section to the bad files section """
        self.xmltree.find(SECTIONS_FINDER.BAD_FUNCTIONS).append(
            etree.XML(FMT.BAD_FUNCTION_FOR_FILE.format(filename))
        )

    def add_function(self, file_section_name, function_name):
        """ add a bad function in its file section in the xml tree """
        bad_function_section = self.xmltree.find(
            SECTIONS_FINDER.BAD_FUNCTIONS_FOR_FILE.format(file_section_name)
        )

        if bad_function_section is None:
            raise NoSection("There is no file section for this function")

        bad_function_section.append(
            etree.XML(FMT.BAD_FUNCTION.format(function_name))
        )
