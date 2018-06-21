#!/usr/bin/python
# coding: utf-8

"""
  Source-Monitor report analyzer. It allows you to analyze a Source-Monitor
  report and check the validity of metrics based on user-defined rules.
"""

from lxml import etree
from utils import center
import reader.smreader as smreader
import entity.files as files
import entity.reports as reports


TITLE_WIDTH = 40


class Analyzer:
    """
        The main analyzer class
    """
    def __init__(self, sm_input, rules_input):
        self.xml_parser = etree.XMLParser(remove_comments=True)

        # Trees
        self.sm_tree = etree.parse(sm_input, parser=self.xml_parser)
        self.rules_tree = etree.parse(rules_input, parser=self.xml_parser)

        # Entity
        self.files = set()
        self.report = None

    def load_files(self):
        """
            Load all the files of the last source-monitor checkpoint
        """
        files_tree = smreader.all_file_pathfinder()(self.sm_tree)[0]
        for file_tree in files_tree:
            # Creating the file and loading all his data
            # print("adding", file_tree.get("file_name"))
            add_file = files.File(file_tree.get("file_name"))
            add_file.load(self.sm_tree, self.rules_tree)

            # Finally add it to the files set
            self.files.add(add_file)

    def make_report(self):
        """ loads the report with the files and analyzes previously done """
        self.report = reports.Report(self.files)

    def print_bad_files(self):  # pragma: no cover
        """ print all the bad files """
        if self.report:
            print(self.report.str_files())
        else:
            print("Report is not loaded")

    def print_bad_functions(self):  # pragma: no cover
        """ print all the bad functions of each file """
        if self.report:
            print(self.report.str_functions())
        else:
            print("Report is not loaded")

    def print_bad_entities(self):  # pragma: no cover
        """ Print all bad function with colors """
        print("-" * TITLE_WIDTH)
        print(center("Bad files", TITLE_WIDTH))
        print("-" * TITLE_WIDTH)
        self.print_bad_files()
        print("\n\n", end='')

        print("-" * TITLE_WIDTH)
        print(center("Bad functions", TITLE_WIDTH))
        print("-" * TITLE_WIDTH)
        self.print_bad_functions()
