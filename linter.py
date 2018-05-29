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
import os
import re

import sublime
import sublime_plugin

from SublimeLinter.lint import NodeLinter


logger = logging.getLogger('SublimeLinter.plugin.eslint')


class ESLint(NodeLinter):
    """Provides an interface to the eslint executable."""

    missing_config_regex = re.compile(
        r'^(.*?)\r?\n\w*(ESLint couldn\'t find a configuration file.)',
        re.DOTALL
    )
    line_col_base = (1, 1)
    defaults = {
        'selector': 'source.js - meta.attribute-with-value',
        'filter_fixables': False,
        'fix_on_save': False
    }

    def should_lint(self, reason):
        self.reason = reason
        return super().should_lint(reason)

    def cmd(self):
        if self.should_attempt_fix():
            return 'eslint --fix-dry-run --format json --stdin --stdin-filename ${file}'

        return 'eslint --format json --stdin --stdin-filename ${file}'

    def should_attempt_fix(self):
        return (
            self.get_view_settings().get('fix_on_save') and
            self.reason == 'on_save' and
            self.view.score_selector(0, 'source.js')
        )

    def on_stderr(self, stderr):
        # Demote 'annoying' config is missing error to a warning.
        if self.missing_config_regex.match(stderr):
            logger.warning(stderr)
            self.notify_failure()
        elif (
            'DeprecationWarning' in stderr or
            'ExperimentalWarning' in stderr or
            'in the next version' in stderr  # is that a proper deprecation?
        ):
            logger.warning(stderr)
        else:
            logger.error(stderr)
            self.notify_failure()

    def find_errors(self, output):
        """Parse errors from linter's output."""
        try:
            # It is possible that users output debug messages to stdout, so we
            # only parse the last line, which is hopefully the actual eslint
            # output.
            # https://github.com/SublimeLinter/SublimeLinter-eslint/issues/251
            last_line = output.rstrip().split(os.linesep)[-1]
            content = json.loads(last_line)
        except ValueError:
            logger.error(
                "JSON Decode error: We expected JSON from 'eslint', "
                "but instead got this:\n{}\n\n"
                "Be aware that we only parse the last line of above "
                "output.".format(output))
            self.notify_failure()
            return

        if logger.isEnabledFor(logging.INFO):
            import pprint
            logger.info(
                '{} output:\n{}'.format(self.name, pprint.pformat(content)))

        filter_fixables = self.get_view_settings().get('filter_fixables')
        for entry in content:
            if 'output' in entry:
                self.replace_buffer_content(entry['output'])

            for match in entry['messages']:
                if match['message'].startswith('File ignored'):
                    continue

                if filter_fixables and 'fix' in match:
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

    def replace_buffer_content(self, content):
        self.view.run_command(
            'sl_eslint_replace_buffer_content', {'text': content})

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

    def run(self, cmd, code):
        # Workaround eslint bug https://github.com/eslint/eslint/issues/9515
        # Fixed in eslint 4.10.0
        if code == '':
            code = ' '

        return super().run(cmd, code)


class sl_eslint_replace_buffer_content(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
