#!/usr/bin/python
# coding: utf-8

"""
  Module that contains finders definition. Finders are made to find specific
  structure/tree through the source-monitor xml report.
"""

from lxml import etree


def last_checkpoint_abs_path():
    """
        Return the absolute path string of the last checkpoint in the
        source-monitor tree.
    """
    return "/sourcemonitor_metrics/project/checkpoints/checkpoint[last()]"


def file_abs_path(filename):
    """
        Return the absolute path string of a file in the source-monitor tree
    """
    return last_checkpoint_abs_path() + "/files/file[@file_name='{}']".format(
        filename
    )


def function_abs_path(source_file, function_name):
    """
        Return the absolute path string of a function in the source-monitor
        tree.
    """
    return file_abs_path(source_file) + \
        "/function_metrics/function[@name='{}']".format(function_name)


def create_file_finder(filename):
    """
        Return a function that search for the file named 'filename'. The
        returned function will find the function from an lxml.etree tree.
        Assuming that I have an xml tree called 'my_xml', that I need to find
        the file 'my_file.c' file. I will use file_finder like this:

        >>> my_file_finder = file_finder('my_file.c')
        >>> my_file_finder(my_xml)
    """
    return etree.XPath(file_abs_path(filename))


def create_function_finder(source_file, func_name):
    """
        Return a function that search for the function named 'func_name' and
        come from the source file named 'source_file'. The returned function
        will find the function from an lxml.etree tree.
        Assuming that I have an xml tree called 'my_xml', that I need to find
        the function 'my_func' into the 'my_file.c' file. I will use
        function_finder like this:

        >>> my_func_finder = function_finder('my_file.c', 'my_func()')
        >>> my_func_finder(my_xml)
    """
    return etree.XPath(function_abs_path(source_file, func_name))
