#!/usr/bin/python
# coding: utf-8

"""
  PySMAnalyzer is a source-monitor report analyzer. It will analyze an XML
  source-monitor checkpoint and say what's wrong according to rules created
  by the user.
"""

import argparse
from lxml import etree

import entity.functions as functions
import entity.files as files
from utils import center


FRAME_SIZE = 70


def options_parser():
    """
        Parse the command line options. Return the an object containing all
        the options and their value
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", dest="test", action="store_true",
                        help="Start all the unit-test of the project")

    return parser.parse_args()


def main():  # pragma: no cover
    """ main du programme. this function is not covered by coverage.py """
    print("*" * FRAME_SIZE)
    print(center("PySMAnalyzer programmed with love by cutty853", FRAME_SIZE))
    options = options_parser()

    if options.test:
        import test
        import test_utils
        import sys

        print(center("Loading all the unit-test of the project", FRAME_SIZE))
        print("*" * FRAME_SIZE)

        test.run()
        test_utils.run()
        sys.exit(0)

    print("*" * FRAME_SIZE, "\n")
    my_func = functions.Function(r"STV\Trieuse\stv\src\ttpdsext.c",
                                 "initttpdsext()")
    my_file = files.File(r"STV\Trieuse\stv\src\ttpdsext.c")

    xml_parser = etree.XMLParser(remove_comments=True)
    tree = etree.parse("samples/sample.xml", parser=xml_parser)
    rules_tree = etree.parse("samples/rules_sample.xml", parser=xml_parser)
    my_func.load_metrics(tree)
    my_func.load_rules(rules_tree)
    my_func.check_validity()
    my_file.load_metrics(tree)
    my_file.load_functions(tree)
    my_file.load_rules(rules_tree)
    my_file.check_validity()

    print(my_func.rules)
    print(my_file.rules)
    print("hey", my_func.validity)
    print("file", my_file.validity)

    print(my_file)
    print(my_func)


if __name__ == "__main__":
    main()
