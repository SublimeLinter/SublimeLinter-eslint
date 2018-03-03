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

import json
import logging
import re
from SublimeLinter.lint import NodeLinter


logger = logging.getLogger('SublimeLinter.plugin.eslint')


class ESLint(NodeLinter):
    """Provides an interface to the eslint executable."""

    npm_name = 'eslint'
    cmd = ('eslint', '--format', 'json', '--stdin', '--stdin-filename', '@')

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
            return

        content = json.loads(output)

        if logger.isEnabledFor(logging.INFO):
            import pprint
            logger.info(
                '{} output:\n{}'.format(self.name, pprint.pformat(content)))

        for entry in content:
            for match in entry['messages']:
                if match['message'].startswith('File ignored'):
                    continue

                yield (
                    match,
                    match['line'] - 1,  # apply line_col_base manually
                    match['column'] - 1,
                    match['ruleId'] if match['severity'] == 2 else '',
                    match['ruleId'] if match['severity'] == 1 else '',
                    match['message'],
                    None  # near
                )

    def reposition_match(self, line, col, m, vv):
        match = m.match
        if match.get('fatal', False):  # parse error
            text = vv.select_line(line)
            return line, 0, len(text)  # select whole line?
            return super().reposition_match(line, col, m, vv)

        # apply line_col_base manually
        end_line = match.get('endLine', line + 1) - 1
        # to ensure a length of 1, add 2 to the starting col
        end_column = match.get('endColumn', col + 2) - 1

        for _line in range(line, end_line):
            text = vv.select_line(_line)
            end_column += len(text)

        return line, col, end_column
