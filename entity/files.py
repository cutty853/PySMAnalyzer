#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

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

    def load_metrics(self, xml_input):
        """
        Description:
            Load the file metrics from the xml_input tree by searching for
            the file's name. Raise the FileNotFound exception if the file's
            name doesn't exist.
        Arguments:
            xml_input: the source-monitor's xml tree
        """
        func_finder = finders.create_file_finder(self.name)
        try:
            file_tree = func_finder(xml_input)[0]
        except IndexError:
            raise FileNotFound("The file doesn't exist !")

        metrics_tree = file_tree[0]

        metrics_dict = {}
        for i in range(int(file_tree[0].get("metric_count"))):
            try:
                metric_value = int(metrics_tree[i].text)
            except ValueError:
                try:
                    metric_value = float(
                        metrics_tree[i].text.replace(",", ".")
                    )
                except ValueError:
                    metric_value = metrics_tree[i].text
            metrics_dict[metrics_tree[i].get("id")] = metric_value

        self.metrics = metrics.FileMetrics(metrics_dict)
