#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by roadhump
# Copyright (c) 2014 roadhump
#
# License: MIT
#

"""This module exports the ESLint plugin class."""

from SublimeLinter.lint import Linter


class ESLint(Linter):

    """Provides an interface to the eslint executable."""

    syntax = ('javascript', 'html')
    cmd = 'eslint'
    regex = (
        r'^.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?:(?P<error>Error)|(?P<warning>Warning)) - '
        r'(?P<message>.+)'
    )
    line_col_base = (1, 0)
    selectors = {
        'html': 'source.js.embedded.html'
    }
    tempfile_suffix = 'js'
    config_file = ('--config', 'eslint.json')
