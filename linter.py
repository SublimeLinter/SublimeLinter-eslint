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
import os
import shutil
from SublimeLinter.lint import NodeLinter, util


logger = logging.getLogger('SublimeLinter.plugin.eslint')


class ESLint(NodeLinter):
    """Provides an interface to the eslint executable."""

    npm_name = 'eslint'
    cmd = 'eslint --format json --stdin --stdin-filename ${file}'

    missing_config_regex = re.compile(
        r'^(.*?)\r?\n\w*(ESLint couldn\'t find a configuration file.)',
        re.DOTALL
    )
    line_col_base = (1, 1)
    defaults = {
        'selector': 'source.js - meta.attribute-with-value'
    }

    def context_sensitive_executable_path(self, cmd):
        """
        Use local eslint only if both local eslint executable and
        local config is found. Fallback to global eslint if exists.
        """
        start_dir = (
            # absolute path of current file
            os.path.abspath(os.path.dirname(self.view.file_name()))
            # or current working directory
            or self.get_working_dir(self.settings)
        )
        local_cmd = self.find_local_linter(start_dir)
        if local_cmd:
            return True, local_cmd

        if self.get_view_settings().get('disable_if_not_dependency', False):
            return True, None

        global_cmd = util.which(cmd[0])
        if global_cmd:
            return True, global_cmd
        else:
            logger.warning('{} cannot locate \'{}\'\n'
                           'Please refer to the readme of this plugin and our troubleshooting guide: '
                           'http://www.sublimelinter.com/en/stable/troubleshooting.html'.format(self.name, cmd[0]))
            return True, None

    def paths_upwards(self, path):
        while True:
            yield path
            next_path = os.path.dirname(path)
            if next_path == path:
                return
            path = next_path

    def has_local_config(self, path):
        eslint_files = [
            ".eslintrc.js",
            ".eslintrc.yaml",
            ".eslintrc.yml",
            ".eslintrc.json",
            ".eslintrc",
        ]
        # Check for existence of config files in current directory
        for config_file in eslint_files:
            if os.path.exists(os.path.join(path, config_file)):
                return True
        return False

    def find_local_linter(self, start_dir, npm_name='eslint'):
        """
        Find local installation of eslint executable
        and return it only if a local config is found.
        """
        config_found = False
        # Check if we have eslint config or executable in package.json
        if self.manifest_path:
            pkg = self.get_manifest()
            pkg_dir = os.path.dirname(self.manifest_path)
            cmd = pkg['bin'][npm_name] if 'bin' in pkg and npm_name in pkg['bin'] else None
            if cmd:
                executable = os.path.normpath(os.path.join(pkg_dir, cmd))
            if 'eslintConfig' in pkg:
                config_found = True

        for path in self.paths_upwards(start_dir):
            node_modules_bin = os.path.join(path, 'node_modules', '.bin')
            executable = shutil.which(npm_name, path=node_modules_bin)
            if not config_found:
                # Look for eslint config in current directory
                config_found = self.has_local_config(path)
            if executable:
                return executable if config_found else None
        else:
            return None

    def on_stderr(self, stderr):
        # Demote 'annoying' config is missing error to a warning.
        if self.missing_config_regex.match(stderr):
            logger.warning(stderr)
            self.notify_failure()
        elif (
            'DeprecationWarning' in stderr
            or 'ExperimentalWarning' in stderr
            or 'in the next version' in stderr  # is that a proper deprecation?
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
            last_line = output.rstrip().split('\n')[-1]
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
            col is None
            or 'endLine' not in match
            or 'endColumn' not in match
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
