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

from SublimeLinter.lint import Linter, util


class ESLint(Linter):

    """Provides an interface to the jshint executable."""

    syntax = ('javascript', 'html')
    cmd = ('eslint')
    tempfile_suffix = 'js'
    regex = (
        r'^(?:(?P<fail>ERROR: .+)|'
        r'.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?:(?P<error>Error)|(?P<warning>Warning)) \- '
        r'(?P<message>.+))'
    )
    selectors = {
        'html': 'source.js.embedded.html'
    }
    config_file = ('--config', '.eslintrc')

    def split_match(self, match):
        """
        Return the components of the match.

        We override this to catch linter error messages and place them
        at the top of the file.

        """

        if match:
            fail = match.group('fail')

            if fail:
                # match, line, col, error, warning, message, near
                return match, 0, 0, True, False, fail, None

        return super().split_match(match)