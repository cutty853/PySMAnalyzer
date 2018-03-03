#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

import utils
import reader.smreader as smreader
import reader.rules_reader as rules_reader
from . import metrics


def create_function_metrics(func_tree):
    """
    Description:
        Return a FunctionMetrics object representing the func_tree passed
    Arguments:
        func_tree: A lxml.etree tree representing a function tree like
        source-monitor's function tree
    """
    return metrics.FunctionMetrics(
        utils.cast_string(func_tree[0].text),
        utils.cast_string(func_tree[1].text),
        utils.cast_string(func_tree[2].text),
        utils.cast_string(func_tree[3].text)
    )


class FunctionNotFound(Exception):
    """ Raised when the function name cannot be found """
    pass


class BadRulesFormat(Exception):
    """ Raised when a tree is not a rules tree """
    pass


class Function:
    """ Represent source-monitor function object """

    def __init__(self, source_file, name):
        self.source_file = source_file
        self.name = name
        self.metrics = None
        self.rules = None

    def __str__(self):
        infos = "Function called {} in {}".format(self.name, self.source_file)
        metrics_string = ""
        if self.metrics:
            metrics_string = " has following metrics:\n  " + \
                str(self.metrics).replace("; ", "\n  ")
        return infos + metrics_string

    def search_tree(self, xml_input):
        """ Return the tree of the function found in the xml_input """
        func_finder = \
            smreader.create_function_finder(self.source_file, self.name)
        try:
            return func_finder(xml_input)[0]
        except IndexError:
            raise FunctionNotFound("The function doesn't exist !")

    def load_metrics(self, xml_input):
        """
        Description:
            Load the function metrics from the xml_input tree by searching for
            the functions's name in the source_file's name. Raise the
            FunctionNotFound exception if the functions's name doesn't exist.
        Arguments:
            xml_input: the source-monitor's xml tree
        """
        func_tree = self.search_tree(xml_input)
        self.metrics = create_function_metrics(func_tree)

    def load_default_rules(self, xml_input):
        """ Load the default metrics rules for the function """
        default_func_rules_finder = rules_reader.default_function_rules_tree()
        try:
            default_rules_tree = default_func_rules_finder(xml_input)[0]
        except IndexError:
            raise BadRulesFormat("Not a rules tree or a corrupted one !")

        self.rules = create_function_metrics(default_rules_tree)

    def load_specific_rules(self, xml_input):
        """ Load the specific rules by modifying the default loaded rules """
        if not self.rules:
            self.load_default_rules(xml_input)

        specific_func_rules_finder = rules_reader.specific_function_rules_tree(
            self.source_file, self.name
        )
        try:
            specific_rules_tree = specific_func_rules_finder(xml_input)[0]
        except IndexError:
            # Their is no rules_tree for this function
            return

        modifiers = {
            "complexity":    self.rules.set_complexity,
            "statements":    self.rules.set_statements,
            "maximum_depth": self.rules.set_maximum_depth,
            "calls":         self.rules.set_calls
        }

        for metric in specific_rules_tree:
            # this test allow comment tag
            if isinstance(metric.tag, str):
                modifiers[metric.tag](utils.cast_string(metric.text))

    def load_rules(self, xml_input):
        """
        Description:
            Load the metrics rules from the xml_input tree (rules tree) by
            loading default rules, then modifying those default rules with
            specific rules
        Arguments:
            xml_input: the parsed rules xml tree
        """
        self.load_default_rules(xml_input)
        self.load_specific_rules(xml_input)
