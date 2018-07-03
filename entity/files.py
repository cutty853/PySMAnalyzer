#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

import utils
import reader.smreader as smreader
import reader.rules_reader as rules_reader
from . import metrics
from . import functions


def create_file_metrics(file_tree):
    """
    Description:
        Return a FileMetrics object representing the file_tree passed
    Arguments:
        file_tree: a lxml.etree tree representing a file tree like
        source-monitor's file tree
    """
    metrics_dict = {
        metric.get("id"): utils.cast_string(metric.text)
        for metric in file_tree
    }
    return metrics.FileMetrics(metrics_dict)


class FileNotFound(Exception):
    """ Raised when the file name cannot be found """
    pass


class File:
    """docstring for File."""
    def __init__(self, name):
        self.name = name
        self.metrics = None
        self.rules = None
        self.validity = True
        self.functions = set()

    def __str__(self):
        infos = "File called {} has {} functions".format(
            self.name, len(self.functions)
        )
        metrics_string = ""
        if self.metrics:
            metrics_string = " has following metrics:\n  " + \
                str(self.metrics).replace("; ", "\n  ")
        return infos + metrics_string

    def search_file_tree(self, xml_input):
        """ Return the function tree of the file found in the xml_input """
        file_finder = smreader.create_file_finder(self.name)
        try:
            return file_finder(xml_input)[0]
        except IndexError:
            raise FileNotFound("The file doesn't exist !")

    def load_metrics(self, xml_input):
        """
        Description:
            Load the file metrics from the xml_input tree by searching for
            the file's name. Raise the FileNotFound exception if the file's
            name doesn't exist.
        Arguments:
            xml_input: the source-monitor's xml tree
        """
        file_tree = self.search_file_tree(xml_input)
        self.metrics = create_file_metrics(file_tree[0])

    def load_functions(self, xml_input):
        """ Load all the functions for the file """
        # Getting the xml tree of the file's functions
        file_tree = self.search_file_tree(xml_input)

        if file_tree[1].tag == "function_metrics":
            functions_tree = file_tree[1]
        else:
            # handles source files that have no functions (no function_metrics)
            functions_tree = []

        # Adding each function to the file's function list
        for function_tree in functions_tree:
            func = functions.Function(self.name, function_tree.get("name"))
            func.load_metrics(xml_input)
            self.functions.add(func)

    def load_default_rules(self, xml_input):
        """ Load the default metrics rules for the function """
        default_file_rules_finder = rules_reader.default_file_rules_tree()
        try:
            default_rules_tree = default_file_rules_finder(xml_input)[0]
        except IndexError:
            raise rules_reader.BadRulesFormat(
                "Not a rules tree or a corrupted one !"
            )

        self.rules = create_file_metrics(default_rules_tree)

    def load_specific_rules(self, xml_input):
        """ Load the specific rules by modifying the default loaded rules """
        if not self.rules:
            self.load_default_rules(xml_input)

        specific_file_rules_finder = rules_reader.specific_file_rules_tree(
            self.name
        )
        try:
            specific_rules_tree = specific_file_rules_finder(xml_input)[0]
        except IndexError:
            # Their is no rules_tree for this file
            return

        for metric in specific_rules_tree[0]:  # iterate over metrics
            self.rules.set(metric.get("id"), utils.cast_string(metric.text))

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

    def check_validity(self):
        """
        Description:
            Check if a file is valid according to its rules
        """
        for metric, rule in zip(self.metrics, self.rules):
            if metrics.is_metric_treatable(metric[1]) and \
               metrics.is_metric_treatable(rule[1]):
                if metric[0] == rule[0] and metric[1] > rule[1]:
                    self.validity = False

    def has_bad_functions(self):
        """ Return True if the file has (a) bad function(s) """
        for function in self.functions:
            if not function.validity:
                return True

        return False

    def load(self, sm_tree, rules_tree):
        """
            Load all the data of the function
        """
        # loading file personnal data
        self.load_metrics(sm_tree)
        self.load_rules(rules_tree)
        self.check_validity()

        # loading functions and their datas
        self.load_functions(sm_tree)
        for function in self.functions:
            function.load(sm_tree, rules_tree)
