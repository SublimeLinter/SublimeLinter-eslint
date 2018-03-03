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

import logging
import re
from SublimeLinter.lint import NodeLinter


logger = logging.getLogger('SublimeLinter.plugin.eslint')


class ESLint(NodeLinter):
    """Provides an interface to the eslint executable."""

    npm_name = 'eslint'
    cmd = ('eslint', '--format', 'compact', '--stdin', '--stdin-filename', '@')

    regex = (
        r'^.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?:(?P<error>Error)|(?P<warning>Warning)) - '
        r'(?P<message>.+)'
    )
    crash_regex = re.compile(
        r'^(.*?)\r?\n\w*(Oops! Something went wrong!)',
        re.DOTALL
    )
    line_col_base = (1, 1)
    defaults = {
        'selector': 'source.js - meta.attribute-with-value'
    }

    def find_errors(self, output):
        """Parse errors from linter's output.

        Log errors when eslint crashes or can't find its configuration.
        """
        match = self.crash_regex.match(output)
        if match:
            logger.error(output)
            return []

        return super().find_errors(output)

    def split_match(self, match):
        """Extract and return values from match.

        Return 'no match' for ignored files
        """
        match, line, col, error, warning, message, near = super().split_match(match)
        if message and message.startswith('File ignored'):
            return match, None, None, None, None, '', None

        return match, line, col, error, warning, message, near
