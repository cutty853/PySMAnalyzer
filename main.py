#!/usr/bin/python
# coding: utf-8

"""
  PySMAnalyzer is a source-monitor report analyzer. It will analyze an XML
  source-monitor checkpoint and say what's wrong according to rules created
  by the user.
"""

import argparse


def options_parser():
    """
        Parse the command line options. Return the an object containing all
        the options and their value
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", dest="test", action="store_true",
                        help="Start all the unit-test of the project")

    return parser.parse_args()


def main():
    """ main du programme """
    print("PySMAnalyzer programmed with love by cutty853")
    options = options_parser()
    if options.test:
        print("Loading all the unit-test of the project")
        import test
        test.run()




if __name__ == "__main__":
    main()
