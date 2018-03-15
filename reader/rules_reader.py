#!/usr/bin/python
# coding: utf-8

"""
  Module that contains finders definition. Finders are made to find specific
  structure/tree through the rules xml file.
"""

from lxml import etree


DEFAULT_FUNCTION_RULES_PATH = "/rules/default/files/function_metrics"
DEFAULT_FILE_RULES_PATH = "/rules/default/files/metrics"


class BadRulesFormat(Exception):
    """ Raised when a tree is not a rules tree """
    pass


def file_abs_path(source_file):
    return "/rules/specific/files/file[@name='{}']".format(source_file)


def function_abs_path(source_file, function_name):
    return file_abs_path(source_file) + \
        "/function_metrics/function[@name='{}']".format(function_name)


def default_function_rules_tree():
    """
        Return a function that search for the default function's rules. The
        returned function will find the rules from an lxml.etree tree.
        Assuming that I have an xml tree called 'my_xml'.
        I will use default_function_rules_tree like this:

        >>> my_rules_finder = default_function_rules_tree()
        >>> my_rules_finder(my_xml)
    """
    return etree.XPath(DEFAULT_FUNCTION_RULES_PATH)


def default_file_rules_tree():
    """
        Return a function that search for the default file's rules. The
        returned function will find the rules from an lxml.etree tree.
        Assuming that I have an xml tree called 'my_xml'.
        I will use default_file_rules_tree like this:

        >>> my_rules_finder = default_file_rules_tree()
        >>> my_rules_finder(my_xml)
    """
    return etree.XPath(DEFAULT_FILE_RULES_PATH)


def specific_function_rules_tree(source_file, function_name):
    """
        Return a function that search for the specific function's rules. The
        returned function will find the rules from an lxml.etree tree.
        Assuming that I have an xml tree called 'my_xml'. That I want to find
        the rules for the function named 'func' which come from the file
        'my_file.c'. I will use default_function_rules_tree like this:

        >>> my_rules_finder = specific_function_rules_tree("my_file.c", "func")
        >>> my_rules_finder(my_xml)
    """
    return etree.XPath(function_abs_path(source_file, function_name))


def specific_file_rules_tree(source_file):
    """
        Return a function that search for the specific function's rules. The
        returned function will find the rules from an lxml.etree tree.
        Assuming that I have an xml tree called 'my_xml'. That I want to find
        the rules for the function named 'func' which come from the file
        'my_file.c'. I will use default_function_rules_tree like this:

        >>> my_rules_finder = specific_function_rules_tree("my_file.c", "func")
        >>> my_rules_finder(my_xml)
    """
    return etree.XPath(file_abs_path(source_file))
