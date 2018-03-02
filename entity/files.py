#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

from lxml import etree
from . import metrics


def create_file_finder(filename):
    """
        Return a function that search for the file named 'filename'. The
        returned function will find the function from an lxml.etree tree.
        Assuming that I have an xml tree called 'my_xml', that I need to find
        the file 'my_file.c' file. I will use file_finder like this:

        >>> my_file_finder = file_finder('my_file.c')
        >>> my_file_finder(my_xml)
    """
    path_format = "/sourcemonitor_metrics/project/checkpoints/" + \
                  "checkpoint[last()]/files/" +                   \
                  "file[@file_name='{}']"
    path = path_format.format(filename)
    return etree.XPath(path)


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
        func_finder = create_file_finder(self.name)
        try:
            file_tree = func_finder(xml_input)[0]
        except IndexError:
            raise FileNotFound("The file doesn't exist !")

        metrics_tree = file_tree[0]
        metrics_dict = {
            metrics_tree[i].get("id"): metrics_tree[i].text for i in range(
                int(file_tree[0].get("metric_count"))
            )
        }
        self.metrics = metrics.FileMetrics(metrics_dict)
