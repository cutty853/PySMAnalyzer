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
    print(center("PySMAnalyzer programmed with {} by cutty853".format(
        colourizer.good("love")
    ), FRAME_SIZE))
    options = options_parser()

    if options.test:
        import test
        # import test_utils
        # import test_analyzer
        import sys

        print(center("Loading all the unit-test of the project", FRAME_SIZE))
        print("*" * FRAME_SIZE)

        test.run()
        # test_utils.run()
        # test_analyzer.run()
        sys.exit(0)

    print("*" * FRAME_SIZE, "\n")

    sm_analyzer = analyzer.Analyzer(
        "samples/sample.xml", "samples/rules_sample.xml"
    )
    sm_analyzer.load_files()
    sm_analyzer.make_report()
    sm_analyzer.print_bad_entities()
    sm_analyzer.report.html()


if __name__ == "__main__":
    main()
