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
import os, re
from SublimeLinter.lint import NodeLinter


class ESLint(NodeLinter):

    """Provides an interface to the eslint executable."""

    syntax = ('javascript', 'html', 'javascriptnext', 'javascript (babel)', 'javascript (jsx)')
    npm_name = 'eslint'
    cmd = ('eslint', '--format', 'compact', '--stdin', '--stdin-filename')
    version_args = '--version'
    version_re = r'v(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.20.0'
    regex = (
        r'^.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?:(?P<error>Error)|(?P<warning>Warning)) - '
        r'(?P<message>.+)'
    )
    line_col_base = (1, 0)
    selectors = {
        'html': 'source.js.embedded.html'
    }
    
    def run(self, cmd, code):
        basename = os.path.basename(self.filename)
        cmd = cmd + [basename, '@']
        str = super(ESLint, self).run(cmd, code)
        if re.match('.*File ignored because of your \.eslintignore file\..*', str):
            return None
        return str
