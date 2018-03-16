#!/usr/bin/python
# coding: utf-8

"""
  Source-Monitor report analyzer. It allows you to analyze a Source-Monitor
  report and check the validity of metrics based on user-defined rules.
"""

from lxml import etree


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

