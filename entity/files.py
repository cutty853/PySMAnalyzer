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

    def search_func_tree(self, xml_input):
        """ Return the function tree of the file found in the xml_input """
        func_finder = smreader.create_file_finder(self.name)
        try:
            return func_finder(xml_input)[0]
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
        file_tree = self.search_func_tree(xml_input)
        self.metrics = create_file_metrics(file_tree[0])

    def load_functions(self, xml_input):
        """ Load all the functions for the file """
        # Getting the xml tree of the file's functions
        file_tree = self.search_func_tree(xml_input)
        functions_tree = file_tree[1]

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

