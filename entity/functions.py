#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

import utils
import reader.smreader as smreader
from . import metrics


class FunctionNotFound(Exception):
    """ Raised when the function name cannot be found """
    pass


class Function:
    """ Represent source-monitor function object """

    def __init__(self, source_file, name):
        self.source_file = source_file
        self.name = name
        self.metrics = None

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

        self.metrics = metrics.FunctionMetrics(
            utils.cast_string(func_tree[0].text),
            utils.cast_string(func_tree[1].text),
            utils.cast_string(func_tree[2].text),
            utils.cast_string(func_tree[3].text)
        )
