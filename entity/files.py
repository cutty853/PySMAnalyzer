#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

import utils
import reader.finders as finders
from . import metrics


class FileNotFound(Exception):
    """ Raised when the file name cannot be found """
    pass


class File:
    """docstring for File."""
    def __init__(self, name=""):
        self.name = name
        self.metrics = None
        self.functions = []

    def __str__(self):
        infos = "File called {} has {} functions".format(
            self.name, len(self.functions)
        )
        metrics_string = ""
        if self.metrics:
            metrics_string = " has following metrics:\n  " + \
                str(self.metrics).replace("; ", "\n  ")
        return infos + metrics_string

    def search_tree(self, xml_input):
        """ Return the tree of the file found in the xml_input """
        func_finder = finders.create_file_finder(self.name)
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
        file_tree = self.search_tree(xml_input)

        metrics_tree = file_tree[0]
        metrics_dict = {
            metrics_tree[i].get("id"): utils.cast_string(metrics_tree[i].text)
            for i in range(int(file_tree[0].get("metric_count")))
        }

        self.metrics = metrics.FileMetrics(metrics_dict)
