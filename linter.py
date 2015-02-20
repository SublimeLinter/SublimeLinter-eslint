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

from SublimeLinter.lint import NodeLinter


class ESLint(NodeLinter):

    """Provides an interface to the eslint executable."""

    syntax = ('javascript', 'html', 'javascriptnext', 'javascript (babel)', 'javascript (jsx)')
    npm_name = 'eslint'
    cmd = 'eslint --format=compact --stdin'
    version_args = '--version'
    version_re = r'v(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.12.0'
    regex = (
        r'^.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?:(?P<error>Error)|(?P<warning>Warning)) - '
        r'(?P<message>.+)'
    )
    line_col_base = (1, 0)
    selectors = {
        'html': 'source.js.embedded.html'
    }
