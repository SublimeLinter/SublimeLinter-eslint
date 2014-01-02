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

    """Provides an interface to the jshint executable."""

    syntax = ('javascript', 'html')
    cmd = ('eslint')
    tempfile_suffix = 'js'
    regex = (
        r'^(.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?P<error>Error) \- '
        r'(?P<message>.+))'
    )
    selectors = {
        'html': 'source.js.embedded.html'
    }
    config_file = ('--config', '.eslintrc')
