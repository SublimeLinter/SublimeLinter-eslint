SublimeLinter-eslint
=========================

This linter plugin for [SublimeLinter][docs] provides an interface to [ESLint](https://github.com/nzakas/eslint). It will be used with files that have the “javascript” syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

### Linter installation
Before using this plugin, you must ensure that `eslint` is installed on your system. To install `eslint`, do the following:

1. Install [Node.js](http://nodejs.org) (and [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) on Linux).

1. Install `eslint` globally by typing the following in a terminal:
   ```
   npm install -g eslint
   ```
Or install `eslint` locally in your project folder:
    ```
    npm install eslint
    ```

1. If you are using `nvm` and `zsh`, ensure that the line to load `nvm` is in `.zprofile` and not `.zshrc`.

1. If you are using `zsh` and `oh-my-zsh`, do not load the `nvm` plugin for `oh-my-zsh`.

Once `eslint` is installed, you must ensure it is in your system PATH so that SublimeLinter can find it. This may not be as straightforward as you think, so please read about [how linter executables are located][locating-executables] in the documentation.

Once you have installed `eslint` you can proceed to install the SublimeLinter-eslint plugin if it is not yet installed.

**Note:** This plugin requires `eslint` 0.9.0 or later.

### Plugin installation
Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `eslint`. Among the entries you should see `SublimeLinter-contrib-eslint`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings][settings]. For information on generic linter settings, please see [Linter Settings][linter-settings].

You can configure `eslint` options in the way you would from the command line, with `.eslintrc` files. For more information, see the [eslint docs](https://github.com/nzakas/eslint/wiki).

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbrevations unless they are very well known.

Thank you for helping out!

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
