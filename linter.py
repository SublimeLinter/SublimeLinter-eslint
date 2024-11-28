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

from functools import partial
import json
import logging
import os
import re
import shutil

import sublime

from SublimeLinter.lint import LintMatch, NodeLinter, PermanentError
from SublimeLinter.lint.base_linter.node_linter import read_json_file
from SublimeLinter.lint.quick_fix import (
    TextRange, QuickAction, merge_actions_by_code_and_line, quick_actions_for)


MYPY = False
if MYPY:
    from typing import Iterator, List, Optional, Union
    from SublimeLinter.lint import util
    from SublimeLinter.lint.linter import VirtualView
    from SublimeLinter.lint.persist import LintError


logger = logging.getLogger('SublimeLinter.plugin.eslint')


STANDARD_SELECTOR = 'source.js, source.jsx'
PLUGINS = {
    'eslint-plugin-html': 'text.html',
    'eslint-plugin-json': 'source.json',
    'eslint-plugin-react': 'source.js, source.jsx, source.mjs, source.cjs, source.ts, source.tsx',
    'eslint-plugin-svelte': 'text.html',
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
        r"^(.*?)\r?\n\w*(ESLint couldn't find a configuration file.)",
        re.DOTALL
    )
    line_col_base = (1, 1)
    defaults = {
        'selector': OPTIMISTIC_SELECTOR,
        '--stdin-filename': '${file:fallback_filename}',
        'prefer_eslint_d': True,
    }

    def find_flat_config(self, start_dir):
        """Find the nearest eslint.config.js file starting from the given directory."""
        current = start_dir
        while current and current != os.path.dirname(current):
            config_path = os.path.join(current, 'eslint.config.js')
            if os.path.isfile(config_path):
                return config_path
            current = os.path.dirname(current)
        return None

    def cmd(self):
        if not self.context.get('file'):
            fallback_filename = self.compute_fallback_filename()
            if fallback_filename:
                self.context['fallback_filename'] = fallback_filename

        cmd = ['eslint', '--format=json', '--stdin']

        # If we have a real file (not a buffer), try to find flat config
        if file_path := self.context.get('file'):
            if config_path := self.find_flat_config(os.path.dirname(file_path)):
                cmd.extend(['--config', config_path])

        return cmd

    def compute_fallback_filename(self):
        # type: () -> Optional[str]
        view_selectors = set(self.view.scope_name(0).split(' '))
        for selector in BUFFER_FILE_EXTENSIONS.keys():
            if selector in view_selectors:
                return '.'.join([BUFFER_FILE_STEM, BUFFER_FILE_EXTENSIONS[selector]])
        return None

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

    def parse_output(self, proc, virtual_view):  # type: ignore[override]
        # type: (util.popen_output, VirtualView) -> Iterator[LintError]
        """Parse errors from linter's output."""
        assert proc.stdout is not None
        assert proc.stderr is not None
        if proc.stderr.strip():
            self.on_stderr(proc.stderr)

        if not proc.stdout:
            self.logger.info('{}: no output'.format(self.name))
            return

        try:
            # It is possible that users output debug messages to stdout, so we
            # only parse the last line, which is hopefully the actual eslint
            # output.
            # https://github.com/SublimeLinter/SublimeLinter-eslint/issues/251
            last_line = proc.stdout.rstrip().split('\n')[-1]
            content = json.loads(last_line)
        except ValueError:
            logger.error(
                "JSON Decode error: We expected JSON from 'eslint', "
                "but instead got this:\n{}\n\n"
                "Be aware that we only parse the last line of above "
                "output.".format(proc.stdout))
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

            for item in entry['messages']:
                if item['message'].startswith('File ignored'):
                    continue

                if 'line' not in item:
                    logger.error(item['message'])
                    self.notify_failure()
                    continue

                match = LintMatch(
                    match=item,
                    filename=filename,
                    line=item['line'] - 1,  # apply line_col_base manually
                    col=_try(lambda: item['column'] - 1),
                    end_line=_try(lambda: item['endLine'] - 1),
                    end_col=_try(lambda: item['endColumn'] - 1),
                    error_type='error' if item['severity'] == 2 else 'warning',
                    code=item.get('ruleId', ''),
                    message=item['message'],
                )
                error = self.process_match(match, virtual_view)
                if error:
                    try:
                        fix_description = item["fix"]
                    except KeyError:
                        pass
                    else:
                        if fix_description:
                            error["fix"] = fix_description  # type: ignore[typeddict-unknown-key]
                    yield error


@quick_actions_for("eslint")
def eslint_fixes_provider(errors, _view):
    # type: (List[LintError], Optional[sublime.View]) -> Iterator[QuickAction]
    def make_action(error):
        # type: (LintError) -> QuickAction
        return QuickAction(
            "eslint: Fix {code}".format(**error),
            partial(eslint_fix_error, error),
            "{msg}".format(**error),
            solves=[error]
        )

    except_ = lambda error: "fix" not in error
    yield from merge_actions_by_code_and_line(make_action, except_, errors, _view)


def eslint_fix_error(error, view) -> "Iterator[TextRange]":
    """
    'fix': {'text': ';  ', 'range': [40, 44]}
    """
    fix_description = error["fix"]
    yield TextRange(
        fix_description["text"],
        sublime.Region(*fix_description["range"])
    )


def _try(getter, otherwise=None, catch=Exception):
    try:
        return getter()
    except catch:
        return otherwise
