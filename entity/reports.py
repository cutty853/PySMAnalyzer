#!/usr/bin/python
# coding: utf-8

"""
  Report entity is the entity that contain the report of the analyzer.
"""


class Report:
    """docstring for Report."""
    def __init__(self, files=None):
        """
        Description:
            Init the Report object. If files is not None, it will make the
            report by loading each attribute value.
        Arguments:
            - files: set(files), default: None, the set of files of a C project
            with checked validity
        """
        self.bad_files = set()
        self.bad_functions = {}
        self.nb_bad_files = 0
        self.nb_bad_functions = 0
        self.nb_bad_functions_for_file = {}

        if files:  # pragma: no cover
            self.make_report(files)

    def load_bad_files(self, files):
        """ load and count how many bad files there are in files """
        for file_ in files:
            if not file_.validity:
                self.bad_files.add(file_)
                self.nb_bad_files += 1

    def new_bad_function(self, filename):
        """ decalre a new set of bad functions for a file """
        self.bad_functions[filename] = set()
        self.nb_bad_functions_for_file[filename] = 0

    def add_bad_function(self, function):
        """ add a bad function to the bad_functions dict """
        try:
            self.bad_functions[function.source_file].add(function)
            self.nb_bad_functions += 1
            self.nb_bad_functions_for_file[function.source_file] += 1
        except KeyError:
            # entry was not initialised
            self.new_bad_function(function.source_file)
            # Retry
            self.add_bad_function(function)

    def load_bad_functions(self, files):
        """
            load and count how many bad functions there are in each file in
            files.
        """
        for file_ in files:
            if file_.has_bad_functions():
                self.new_bad_function(file_.name)

                for function in file_.functions:
                    if not function.validity:
                        self.add_bad_function(function)

    def make_report(self, files):
        """ Make the report from a set of files """
        self.load_bad_files(files)
        self.load_bad_functions(files)
