#!/usr/bin/python
# coding: utf-8

"""
  Report entity is the entity that contain the report of the analyzer.
"""

# IDEA: Construire le rapport écrit (string ou html) grace a un générateur
# pour print au fur et a mesure à l'écran ou dans un fichier

from utils import colourizer
import writer.htmlreport as htmlreport
import writer.xmlreport as xmlreport
from entity.metrics import FunctionMetrics, FileMetrics


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
        # {"bonjour.c": set("hello()", "au_revoir()")}
        self.bad_functions = {}
        # {
        #     "bonjour.c": {
        #         "hello()": FunctionMetrics(),
        #         "au_revoir()": FunctionMetrics()
        #     }
        # }
        self.bad_functions_metrics = {}
        self.nb_bad_files = 0
        self.nb_bad_functions = 0
        self.nb_bad_functions_for_file = {}

        self.html_report = htmlreport.HTMLReporter()
        self.xml_report = xmlreport.XMLReporter()

        if files:  # pragma: no cover
            self.make_report(files)

    def load_bad_files(self, files):
        """ load and count how many bad files there are in files """
        for file_ in files:
            if not file_.validity:
                self.bad_files.add(file_)
                self.nb_bad_files += 1

    def new_bad_functions(self, filename):
        """ decalre a new set of bad functions for a file """
        self.bad_functions[filename] = set()
        self.bad_functions_metrics[filename] = dict()
        self.nb_bad_functions_for_file[filename] = 0

    def add_bad_function(self, function):
        """ add a bad function to the bad_functions dict """
        def is_valid(metric_name):
            """ check if a function metrics is valid """
            return metric_name in function.non_valid_metrics

        filename = function.source_file
        try:
            self.bad_functions[filename].add(function)
            self.bad_functions_metrics[filename][function.name] = FunctionMetrics(
                complexity=is_valid("complexity"),
                statements=is_valid("statements"),
                maximum_depth=is_valid("maximum_depth"),
                calls=is_valid("calls")
            )
            self.nb_bad_functions_for_file[filename] += 1
            self.nb_bad_functions += 1
        except KeyError:
            # entry was not initialised
            self.new_bad_functions(filename)
            # Retry
            self.add_bad_function(function)

    def load_bad_functions(self, files):
        """
            load and count how many bad functions there are in each file in
            files.
        """
        for file_ in files:
            if file_.has_bad_functions():
                self.new_bad_functions(file_.name)

                for function in file_.functions:
                    if not function.validity:
                        self.add_bad_function(function)

    def make_report(self, files):
        """ Make the report from a set of files """
        self.load_bad_files(files)
        self.load_bad_functions(files)

    def worst_file_name(self):
        # TODO: Trouver et tester la méthode la plus efficace (test d'implémentation ou fonctionnel)
        v = list(self.nb_bad_functions_for_file.values())
        k = list(self.nb_bad_functions_for_file.keys())
        return k[v.index(max(v))]

    ###########################################################################
    #                           STRING CONVERSION                             #
    ###########################################################################

    def str_files(self):
        """ convert the files' report part into string """
        # TODO: Load file metrics names correspondance
        return "\n".join([
            "File {} has bad metrics ({})".format(
                colourizer.color_file(file_.name),
                file_.non_valid_metrics
            )
            for file_ in self.bad_files
        ])

    def str_functions(self):
        """ convert the functions's report part into string """
        return "".join([
            "File {}\n".format(colourizer.color_file(filename)) +
            "".join([
                "{} Function {} from {} has bad metrics ({})\n".format(
                    colourizer.error("■"),
                    colourizer.color_function(function.name),
                    filename,
                    function.non_valid_metrics
                )
                for function in functions
            ]) + "\n"
            for filename, functions in self.bad_functions.items()
        ])

    ###########################################################################
    #                            HTML CONVERSION                              #
    ###########################################################################

    def html(self):
        """ convert the report into html """
        self.html_report.load_layout()

        self.html_files()
        self.html_functions()
        self.html_infos()

        return self.html_report.convert().decode()

    def html_infos(self):
        """ convert the report's infos part into html """
        self.html_report.change_bad_files_amount(self.nb_bad_files)
        self.html_report.change_bad_functions_amount(self.nb_bad_functions)
        self.html_report.change_worst_file_name(self.worst_file_name())

    def html_files(self):
        """ convert the files' report part into html """
        for file_ in self.bad_files:
            self.html_report.add_file(file_.name)

    def html_functions(self):
        """ convert the functions' report part into html """
        for filename, functions in self.bad_functions.items():
            self.html_report.add_file_section(filename)
            for function in functions:
                self.html_report.add_function(filename, function.name)

    ###########################################################################
    #                             XML CONVERSION                              #
    ###########################################################################

    # TODO: Extract a converter methods from the html and the xml converter

    def xml(self):
        self.xml_report.load_layout()

        self.xml_files()
        self.xml_functions()

        return self.xml_report.convert().decode()

    def xml_files(self):
        """ convert the files' report part into html """
        for file_ in self.bad_files:
            self.xml_report.add_file(file_.name)

    def xml_functions(self):
        """ convert the functions' report part into html """
        for filename, functions in self.bad_functions.items():
            self.xml_report.add_file_section(filename)
            for function in functions:
                self.xml_report.add_function(filename, function.name)
