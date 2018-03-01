#!/usr/bin/python
# coding: utf-8

"""
  Module that define all sorts of metrics
"""


class FunctionMetrics:
    def __init__(self, complexity=0, statements=0, maximum_depth=0, calls=0):
        self.complexity = complexity
        self.statements = statements
        self.maximum_depth = maximum_depth
        self.calls = calls
