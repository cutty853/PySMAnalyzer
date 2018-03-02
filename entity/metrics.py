#!/usr/bin/python
# coding: utf-8

"""
  Module that define all sorts of metrics
"""


class FileMetrics:
    def __init__(self, metrics):
        self._metrics = metrics.copy()

    def __str__(self):
        return "; ".join(
            [id_ + ": " + str(value) for id_, value in self._metrics.items()]
        )

    def get(self, id_name):
        """ Return the value of the metrics named id_name """
        return self._metrics[id_name]


class FunctionMetrics:
    def __init__(self, complexity=0, statements=0, maximum_depth=0, calls=0):
        self.complexity = complexity
        self.statements = statements
        self.maximum_depth = maximum_depth
        self.calls = calls

    def __str__(self):
        f_string = \
            "complexity: {}; statements: {}; maximum_depth: {}; calls: {}"
        return f_string.format(
            self.complexity, self.statements, self.maximum_depth, self.calls
        )
