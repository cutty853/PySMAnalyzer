#!/usr/bin/python
# coding: utf-8

"""
  PySMAnalyzer is a source-monitor report analyzer. It will analyze an XML
  source-monitor checkpoint and say what's wrong according to rules created
  by the user.
"""

import argparse
from utils import center, colourizer
import analyzer


FRAME_SIZE = 70


def define_parser():
    """
        Parse the command line options. Return the an object containing all
        the options and their value
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", dest="test", action="store_true",
                        help="Start all the unit-test of the project")

    parser.add_argument("-o", "--output", dest="output",
                        help="The output file")
    parser.add_argument("-f", "--fomat", dest="format", default="html",
                        help="output format, default: html")
    parser.add_argument("input", help="source monitor input file", nargs="?")
    parser.add_argument("rules", help="rules file", nargs="?")

    return parser


def main():  # pragma: no cover
    """ main du programme. this function is not covered by coverage.py """
    print("*" * FRAME_SIZE)
    print(center("PySMAnalyzer programmed with {} by cutty853".format(
        colourizer.good("love")
    ), FRAME_SIZE))
    parser = define_parser()
    options = parser.parse_args()

    if options.test:
        import test
        import sys

        print(center("Loading all the unit-test of the project", FRAME_SIZE))
        print("*" * FRAME_SIZE)

        result = test.run()
        sys.exit(not result)

    print("*" * FRAME_SIZE, "\n")

    if not options.input or not options.rules:
        import sys
        print("You must provide a input file and a rules file")
        print("-" * FRAME_SIZE)
        parser.print_help()
        sys.exit(1)
    if options.format not in {"html", "xml"}:
        import sys
        print("You must provide a supported format (html or xml)")
        print("-" * FRAME_SIZE)
        parser.print_help()
        sys.exit(1)

    sm_analyzer = analyzer.Analyzer(options.input, options.rules)
    sm_analyzer.load_files()
    sm_analyzer.make_report()
    sm_analyzer.print_bad_entities()
    if options.output:
        sm_analyzer.save_report(options.output, method=options.format)


if __name__ == "__main__":
    main()
