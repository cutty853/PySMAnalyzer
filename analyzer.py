#!/usr/bin/python
# coding: utf-8

"""
  Source-Monitor report analyzer. It allows you to analyze a Source-Monitor
  report and check the validity of metrics based on user-defined rules.
"""

from lxml import etree
from utils import colourizer, center
import reader.smreader as smreader
import entity.files as files


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

    def print_bad_files(self):  # pragma: no cover
        """ print all the bad files """
        for file_ in self.files:
            if not file_.validity:
                print("File {} has bad metrics".format(
                    colourizer.color_file(file_.name)
                ))

    def print_bad_functions(self):  # pragma: no cover
        """ print all the bad functions of each file """
        for file_ in self.files:
            if file_.has_bad_functions():
                print("File", colourizer.color_file(file_.name))

                for function in file_.functions:
                    if not function.validity:
                        print("{} Function {} from {} has bad metrics".format(
                            colourizer.error("■"),
                            colourizer.color_function(function.name),
                            file_.name
                        ))

                print()

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
