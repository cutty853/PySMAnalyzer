#!/usr/bin/python
# coding: utf-8

"""
  Source-Monitor report analyzer. It allows you to analyze a Source-Monitor
  report and check the validity of metrics based on user-defined rules.
"""

from lxml import etree
import reader.smreader as smreader
import entity.files as files


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

    def print_files(self):  # pragma: no cover
        for file_ in self.files:
            print("file", file_.name)
            print(file_.validity)
            print("functions")
            for function in file_.functions:
                print(function.validity)
