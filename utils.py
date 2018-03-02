#!/usr/bin/python
# coding: utf-8

"""
  utilitary module
"""


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