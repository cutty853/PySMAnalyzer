#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

import reader.finders as finders
from . import metrics


class FunctionNotFound(Exception):
    """ Raised when the function name cannot be found """
    pass


class Function:
    """ Represent source-monitor function object """

    def __init__(self, source_file="", name=""):
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

    def load_metrics(self, xml_input):
        """
        Description:
            Load the function metrics from the xml_input tree by searching for
            the functions's name in the source_file's name. Raise the
            FunctionNotFound exception if the functions's name doesn't exist.
        Arguments:
            xml_input: the source-monitor's xml tree
        """
        func_finder = \
            finders.create_function_finder(self.source_file, self.name)
        try:
            func_tree = func_finder(xml_input)[0]
        except IndexError:
            raise FunctionNotFound("The function doesn't exist !")

        # Here we assume that sm file won't contain "impossible to int" text
        self.metrics = metrics.FunctionMetrics(
            int(func_tree[0].text),
            int(func_tree[1].text),
            int(func_tree[2].text),
            int(func_tree[3].text)
        )
