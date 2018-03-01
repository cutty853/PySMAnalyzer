#!/usr/bin/python
# coding: utf-8

"""
  Module for the function entity
"""

from . import metrics


class Function:
    """ Represent source-monitor function object """

    def __init__(self):
        self.source_file = ""
        self.name = ""
        self.metrics = None

    def __str__(self):
        return str(self)
