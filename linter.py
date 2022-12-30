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
import shutil
from SublimeLinter.lint import LintMatch, NodeLinter, PermanentError

from SublimeLinter.lint.base_linter.node_linter import read_json_file


MYPY = False
if MYPY:
    from typing import List, Union


logger = logging.getLogger('SublimeLinter.plugin.eslint')


STANDARD_SELECTOR = 'source.js, source.jsx'
PLUGINS = {
    'eslint-plugin-html': 'text.html',
    'eslint-plugin-json': 'source.json',
    'eslint-plugin-svelte3': 'text.html',
    'eslint-plugin-vue': 'text.html.vue',
    '@angular-eslint/eslint-plugin': 'text.html',
    '@typescript-eslint/parser': 'source.ts, source.tsx',
    'tsdx': 'source.ts, source.tsx',
    'eslint-plugin-yml': 'source.yaml',
    'eslint-plugin-yaml': 'source.yaml',
}
OPTIMISTIC_SELECTOR = ', '.join({STANDARD_SELECTOR} | set(PLUGINS.values()))

BUFFER_FILE_STEM = '__buffer__'
BUFFER_FILE_EXTENSIONS = {
    'source.js': 'js',
    'source.jsx': 'jsx',
    'text.html': 'html',
    'text.html.vue': 'vue',
    'source.ts': 'ts',
    'source.tsx': 'tsx',
    'source.json': 'json',
    'source.yaml': 'yaml',
}


class ESLint(NodeLinter):
    """Provides an interface to the eslint executable."""

    missing_config_regex = re.compile(
        r'^(.*?)\r?\n\w*(ESLint couldn\'t find a configuration file.)',
        re.DOTALL
    )
    line_col_base = (1, 1)
    defaults = {
        'selector': OPTIMISTIC_SELECTOR,
        'prefer_eslint_d': True,
    }

    def cmd(self):
        cmd = ['eslint', '--format=json', '--stdin']
        stdin_filename = self.get_stdin_filename()
        if stdin_filename:
            cmd.append('--stdin-filename=' + stdin_filename)
        return cmd

    def run(self, cmd, code):
        # Workaround eslint bug https://github.com/eslint/eslint/issues/9515
        # Fixed in eslint 4.10.0
        if code == '':
            code = ' '

        self.ensure_plugin_installed()
        return super().run(cmd, code)

    def ensure_plugin_installed(self) -> bool:
        # If the user changed the selector, we take it as is
        if self.settings['selector'] != OPTIMISTIC_SELECTOR:
            return True

        # Happy path.
        if self.view.match_selector(0, STANDARD_SELECTOR):
            return True

        # If we're here we must be pessimistic.

        # The 'project_root' has the relevant 'package.json' file colocated.
        # If we fallback to a global installation there is no 'project_root',
        # t.i. no auto-selector in that case as well.
        project_root = self.context.get('project_root')
        if not project_root:
            logger.info("No project_root found.")
            if 'executable' in self.settings:
                logger.info(
                    "If 'executable' is set in settings, 'selector' "
                    "should also manually be specified.")
            self.notify_unassign()  # Abort linting without popping error dialog
            raise PermanentError()

        # We still need to be careful, in case SL deduced a 'project_root'
        # without checking for the 'package.json' explicitly. Basically, a
        # happy path for SL core.
        manifest_file = os.path.join(project_root, 'package.json')
        try:
            manifest = read_json_file(manifest_file)
        except Exception as exc:
            logger.info(
                "Failed to read package.json at project_root '{}' to determine "
                "whether or not to eslint this file".format(project_root))
            logger.info(exc)
            # Occurs even if file not found, so don't notify
            self.notify_unassign()  # Abort linting without popping error dialog
            raise PermanentError()

        defined_plugins = PLUGINS.keys() & (
            manifest.get('dependencies', {}).keys()
            | manifest.get('devDependencies', {}).keys()
        )
        selector = ', '.join(PLUGINS[name] for name in defined_plugins)
        if selector and self.view.match_selector(0, selector):
            return True

        logger.info(
            "package.json did not contain dependencies or devDependencies "
            "required to lint this file type. Manually set 'selector' to "
            "override this behavior, or install the required dependencies.")
        self.notify_unassign()  # Abort linting without popping error dialog
        raise PermanentError()

    def get_stdin_filename(self) -> str | None:
        filename = self.view.file_name()
        if filename is None:
            view_selectors = set(self.view.scope_name(0).split(' '))
            for selector in BUFFER_FILE_EXTENSIONS.keys():
                if selector in view_selectors:
                    filename = '.'.join([BUFFER_FILE_STEM, BUFFER_FILE_EXTENSIONS[selector]])
                    break
        return filename

    def find_local_executable(self, start_dir, npm_name):
        # type: (str, str) -> Union[None, str, List[str]]
        """Automatically switch to `eslint_d` if available (and wanted)."""
        executable = super().find_local_executable(start_dir, npm_name)
        if self.settings.get('prefer_eslint_d') and isinstance(executable, str):
            basedir = os.path.dirname(executable)
            daemonized_name = '{}_d'.format(npm_name)
            return (
                (shutil.which(daemonized_name, path=basedir) if basedir else None)  # local
                or self.which(daemonized_name)         # global
                or executable                          # keep it
            )

        return executable

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
            filename = entry.get('filePath', None)
            if filename == '<text>':
                filename = 'stdin'
            elif filename and os.path.basename(filename).startswith(BUFFER_FILE_STEM + '.'):
                filename = 'stdin'

            for match in entry['messages']:
                if match['message'].startswith('File ignored'):
                    continue

                if 'line' not in match:
                    logger.error(match['message'])
                    self.notify_failure()
                    continue

                yield LintMatch(
                    match=match,
                    filename=filename,
                    line=match['line'] - 1,  # apply line_col_base manually
                    col=_try(lambda: match['column'] - 1),
                    end_line=_try(lambda: match['endLine'] - 1),
                    end_col=_try(lambda: match['endColumn'] - 1),
                    error_type='error' if match['severity'] == 2 else 'warning',
                    code=match.get('ruleId', ''),
                    message=match['message'],
                )


def _try(getter, otherwise=None, catch=Exception):
    try:
        return getter()
    except catch:
        return otherwise
