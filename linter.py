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
    cmd = 'eslint --format json --stdin --stdin-filename ${file}'

    missing_config_regex = re.compile(
        r'^(.*?)\r?\n\w*(ESLint couldn\'t find a configuration file.)',
        re.DOTALL
    )
    crash_regex = re.compile(
        r'^(.*?)\r?\n\w*(Oops! Something went wrong!)',
        re.DOTALL
    )
    line_col_base = (1, 1)
    defaults = {
        'selector': 'source.js - meta.attribute-with-value'
    }

    def on_stderr(self, stderr):
        # Demote 'annoying' config is missing error to a warning.
        if self.missing_config_regex.match(stderr):
            logger.warning(stderr)
            self.notify_failure()
        elif 'in the next version' in stderr:  # is that a proper deprecation?
            logger.warning(stderr)
        else:
            logger.error(stderr)
            self.notify_failure()

    def find_errors(self, output):
        """Parse errors from linter's output."""
        try:
            content = json.loads(output)
        except ValueError:
            logger.error('{} output:\n{}'.format(self.name, output))
            self.notify_failure()
            return

        if logger.isEnabledFor(logging.INFO):
            import pprint
            logger.info(
                '{} output:\n{}'.format(self.name, pprint.pformat(content)))

        for entry in content:
            for match in entry['messages']:
                if match['message'].startswith('File ignored'):
                    continue

                column = match.get('column', None)
                ruleId = match.get('ruleId', '')
                if column is not None:
                    # apply line_col_base manually
                    column = column - 1

                yield (
                    match,
                    match['line'] - 1,  # apply line_col_base manually
                    column,
                    ruleId if match['severity'] == 2 else '',
                    ruleId if match['severity'] == 1 else '',
                    match['message'],
                    None  # near
                )

    def reposition_match(self, line, col, m, vv):
        match = m.match
        if (
            col is None or
            'endLine' not in match or
            'endColumn' not in match
        ):
            return super().reposition_match(line, col, m, vv)

        # apply line_col_base manually
        end_line = match['endLine'] - 1
        end_column = match['endColumn'] - 1

        for _line in range(line, end_line):
            text = vv.select_line(_line)
            end_column += len(text)

        return line, col, end_column
