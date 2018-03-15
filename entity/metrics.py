#!/usr/bin/python
# coding: utf-8

"""
  Module that define all sorts of metrics
"""


class FileMetrics:
    """ The class represent the metrics of a file """

    def __init__(self, metrics):
        self._metrics = metrics.copy()

    def __str__(self):
        return "; ".join(
            [id_ + ": " + str(value) for id_, value in self._metrics.items()]
        )

    def get(self, id_name):
        """ Return the value of the metrics named id_name """
        return self._metrics[id_name]

    def set(self, id_name, new_value):
        """ setter for the metrics named id_name """
        self._metrics[id_name] = new_value


class FunctionMetrics:
    """ The class represent the metrics of a function """

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

    def __iter__(self):
        yield self.complexity
        yield self.statements
        yield self.maximum_depth
        yield self.calls

    def set_complexity(self, complexity):
        """ complexity setter """
        self.complexity = complexity

    def set_statements(self, statements):
        """ statements setter """
        self.statements = statements

    def set_maximum_depth(self, maximum_depth):
        """ maximum_depth setter """
        self.maximum_depth = maximum_depth

    def set_calls(self, calls):
        """ calls setter """
        self.calls = calls
