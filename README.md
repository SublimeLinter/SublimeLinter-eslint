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
Or install `eslint` locally in your project folder (**you must have package.json file there**):
    ```
    npm init -f
    npm install eslint
    ```

1. Init `eslint` config if you don't have any. Run in your code folder:

    ```
    eslint --init
    ```

    or if `eslint` is installed locally

    ```
    ./node_modules/.bin/eslint --init
    ```

Reopen your project next (or restart ST) to make sure local `eslint` will be used.

1. If you are using `nvm` and `zsh`, ensure that the line to load `nvm` is in `.zprofile` and not `.zshrc`.

1. If you are using `zsh` and `oh-my-zsh`, do not load the `nvm` plugin for `oh-my-zsh`.

Once `eslint` is installed, you must ensure it is in your system PATH so that SublimeLinter can find it. This may not be as straightforward as you think, so please read about [how linter executables are located][locating-executables] in the documentation.

Once you have installed `eslint` you can proceed to install the SublimeLinter-eslint plugin if it is not yet installed.

**Note:** This plugin requires `eslint` 1.0.0 or later.

### Plugin installation
Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `eslint`. Among the entries you should see `SublimeLinter-contrib-eslint`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings][settings]. For information on generic linter settings, please see [Linter Settings][linter-settings].

You can configure `eslint` options in the way you would from the command line, with `.eslintrc` files. For more information, see the [eslint docs](https://github.com/nzakas/eslint/wiki).

## FAQ and Troubleshooting

##### What is my first step to find out what trouble I have?

Use SublimeText console and SublimeLinter debug mode.

1. Check `Tools -> SublimeLinter -> Debug Mode`.
2. Open console `View -> Show Console`.

Then open any JS file and run `Tools -> SublimeLinter -> Lint This View`. It must be an output in console after, something like that:

```
SublimeLinter: eslint: 1.js ['/Projects/sample/node_modules/.bin/eslint', '--format', 'compact', '--stdin', '--stdin-filename', '@'] 
```

##### I've got 'SublimeLinter: ERROR: eslint cannot locate 'eslint' in ST console when I try to use locally installed `eslint`.

You **must** have `package.json` file if install `eslint` locally. Also, restart project or ST itself after to make sure SublimeLinter uses correct `eslint` instance.

```
npm init -f
npm install eslint
```

##### Plugin still does not work or there are errors in ST console.

Update `eslint` instance, probably you use outdated version and SublimeLinter does not check it properly sometimes.

##### There are no errors in console, but plugin does nothing.

ESLint >2.0.0 does not enable any default rules and you should have config file for your code. Run in your console:
```
eslint --init # if eslint is global
./node_modules/.bin/eslint --init # if eslint is installed locally
```

##### I want plugin to use my `.eslintignore` settings.

~~It does it now.~~

###### For ESLint <2.0.0

Add to your SublimeLinter settings (global or per-project):

```json
{
    "linters": {
        "eslint": {
            "args": [
                "--stdin-filename", "__RELATIVE_TO_FOLDER__"
            ]
        }
    }
}
```

It can limit some rules and probably cause some bugs (i.e. files in symlinked folders can be skipped).

###### For ESLint >=2.0.0 or if previous solution can't be applied

Duplicate ESLint ignore settings to your `.sublimelinterrc` file. Use double stars for correct match.

```json
{
    "linters": {
        "eslint": {
            "excludes": [
                "**/node_modules/**",
                "**/vendor/**"
            ]
        }
    }
}

```

###### For ESLint >=2.0.0

If you use a SublimeText project and `.sublime-project` file is in project folder, set `chdir` to `${project}` in your SublimeLinter settings. **Warning:** it can cause bugs if your project has more than one root folder.

##### I want not to lint files if there is no `.eslintrc` file in project folder (for ESLint <1.0.0).

Use `--reset` [ESLint](http://eslint.org/docs/user-guide/command-line-interface#reset) option, add it to your SublimeLinter global settings or project `.sublimelinterrc` file as below. Add `--no-reset` option to project `.sublimelinterrc` to overwrite it back.

```json
{
    "linters": {
        "eslint": {
            "args": [
                "--reset"
            ]
        }
    }
}
```

##### I want to use global `.eslintrc` config.

Plugin uses the same [configuration hierarchy](http://eslint.org/docs/user-guide/configuring#configuration-cascading-and-hierarchy) as `eslint` itself, so add `.eslintrc` to your home directory or ancestor directory of project.

##### I want to use custom rules, global `.eslintignore` file, etc.

You can specify **any** [CLI options](http://eslint.org/docs/user-guide/command-line-interface#options) of `eslint` with `args` key in SublimeLinter configs.

```json
{
    "linters": {
        "eslint": {
            "args": [
                "--ignore-path", "~/eslint_ignore",
                "--rulesdir", "~/rules"
            ]
        }
    }
}
```

##### There is no `SublimeLinter-contrib-eslint` package to install in Package Control packages list.

Check if you already have it installed, please.

##### It's not linting for JSX.

Try changing your syntax from JSX to Babel > Javascript. ([ref issue](https://github.com/roadhump/SublimeLinter-eslint/issues/106))

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, so don’t be afraid to use it.
- Please use descriptive variable names, so no abbreviations unless they are very well known.

Thank you for helping out!

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
[eslint_d]: https://github.com/mantoni/eslint_d.js
