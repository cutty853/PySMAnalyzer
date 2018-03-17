#!/usr/bin/python
# coding: utf-8

"""
  utilitary module
"""


class ProgColors:
    """ Enumerate the colors of the programm for bash printing """
    def __init__(self):
        self.CLEAN = '\033[0m'
        self.FUNCTION_NAME = '\033[36m'  # Cyan
        self.FILE_NAME = '\033[33m'  # Yellow
        self.ERROR = '\033[31m'  # Red
        self.GOOD = '\033[32m'  # Green

    def error(self, text):
        """ frame texte with the error color """
        return self.ERROR + text + self.CLEAN

    def good(self, text):
        """ frame texte to show it has 'good' """
        return self.GOOD + text + self.CLEAN

    def color_function(self, text):
        """ frame text supposed to be a function name """
        return self.FUNCTION_NAME + text + self.CLEAN

    def color_file(self, text):
        """ frame texte supposed to be a file name """
        return self.FILE_NAME + text + self.CLEAN

    def disable(self):
        """ disable all colors """
        self.CLEAN = ''
        self.FUNCTION_NAME = ''  # Cyan
        self.FILE_NAME = ''  # Yellow
        self.ERROR = ''  # Red
        self.GOOD = ''  # Green


colourizer = ProgColors()  # pylint: disable=invalid-name


def center(message, max_line_size):
    """
        Return a string where message is centered relative to the size of a
        line. It doesn't break the message if its behond max_line_size
    """
    message_lenght = len(message)

    if message_lenght > max_line_size:
        return message

    padding = ((max_line_size - message_lenght) // 2) * " "
    return padding + message + padding


def cast_string(string):
    """ Convert a string to the implicit type of its content """
    if not string:
        return ""

    try:
        return int(string)
    except ValueError:
        pass

    try:
        return float(string.replace(",", "."))
    except ValueError:
        pass

    return string
