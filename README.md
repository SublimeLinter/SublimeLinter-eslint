SublimeLinter-eslint
=========================

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [ESLint](https://github.com/nzakas/eslint). It will be used with "JavaScript" files, but since `eslint` is pluggable, it can actually lint a variety of other files as well.

## Installation
SublimeLinter must be installed in order to use this plugin.

Please install via [Package Control](https://packagecontrol.io).

Before using this plugin, ensure that `eslint` is installed on your system.
To install `eslint`, do the following:

- Install [Node.js](http://nodejs.org) (and [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) on Linux).

- Install `eslint` globally by typing the following in a terminal:
```
npm install -g eslint
```
    
- Or install `eslint` locally in your project folder (**you must have a `package.json` file there**):
```
npm install -D eslint
```

## Quick Fixes

`eslint` provides fixes for some errors.  These fixes are available in SublimeLinter as quick actions. See the Command Palette: `SublimeLinter: Quick Action`.  (Also: https://github.com/SublimeLinter/SublimeLinter#quick-actionsfixers)

You may want to define a key binding:

```
    // To trigger a quick action
    { "keys": ["ctrl+k", "ctrl+f"],
      "command": "sublime_linter_quick_actions"
    },
```

## Using eslint with plugins (e.g. vue)

SublimeLinter will detect _some_ installed **local** plugins, and thus it should work automatically for e.g. `.vue` or `.ts` files. If it works on the command line, there is a chance it works in Sublime without further ado.  

- Make sure the plugins are installed **locally** colocated to `eslint` itself. T.i., technically, both `eslint` and its plugins are described in the very same `package.json`. 
- Configuration of the plugins is out-of-scope of this README. Be sure to read _their_ README's as well. (If you just installed a plugin, without proper configuration, `eslint` will probably show error messages or wrong lint results, and SublimeLinter will just pass them to you.)

Out-of-the-box SublimeLinter detects typescript, vue, svelte, html, and json. Please open a PR for important other plugins. Note, however, that when you configure the `executable` manually, you also opt-out of the automatic plugin detection and fallback to linting "Javscript" only. 

In any case, if you want to control which files SublimeLinter sends to `eslint`, you can always manually change the `"selector"` setting to just include the scopes you explicitly want. The default value for "JavaScript" is `source.js - meta.attribute-with-value`, make sure to include that in the configuration. 

### Examples

For [Typescript](https://www.typescriptlang.org/) `.ts` files it would be:

```json
"linters": {
    "eslint": {
        "selector": "source.ts, source.js - meta.attribute-with-value"
    }
}
```

For [Vue.js](https://vuejs.org/) `.vue` files it would be:

```json
"linters": {
    "eslint": {
        "selector": "text.html.vue, source.js - meta.attribute-with-value"
    }
}
```

For [Svelte](https://svelte.dev/) `.svelte` files, using [`eslint-plugin-svelte`](https://github.com/sveltejs/eslint-plugin-svelte) and [Svelte](https://packagecontrol.io/packages/Svelte) syntax highlighting, it would be:

```json
"linters": {
    "eslint": {
        "selector": "text.html.svelte, source.js - meta.attribute-with-value"
    }
}
```

To find the `selector` value for a particular file type, place the cursor at the start of the file and use the command **Tools** ➡️ **Developer** ➡️ **Show Scope Name**.

## Using eslint_d

This plugin will automatically prefer a `eslint_d` installation if present.
You can change this behavior by setting `prefer_eslint_d` to `false` either
globally or per project.  E.g. for the global setting:

```json
"linters": {
    "eslint": {
        "prefer_eslint_d": false
    }
}
```

## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

You can configure `eslint` options in the way you would from the command line, with `.eslintrc` files. For more information, see the [eslint docs](https://github.com/nzakas/eslint/wiki).


## FAQ and Troubleshooting

### `eslint` doesn't lint my HTML files anymore.

Starting with v4.2 of this plugin, `eslint` will only lint '*.js' files for standard, vanilla configurations without further plugins. You can restore the old behavior by setting `selector` to its old value: 

```json
"linters": {
    "eslint": {
        "selector": "source.js - meta.attribute-with-value"
    }
}
```

### I've got 'SublimeLinter: ERROR: eslint cannot locate 'eslint' in ST console when I try to use locally installed `eslint`.

You **must** have a `package.json` file if you've installed `eslint` locally. Also, restart the project or Sublime Text itself after to make sure SublimeLinter uses the correct `eslint` instance.

```
npm init -f
npm install eslint
```

### I've got 'SublimeLinter: eslint ERROR: ESLint couldn't find a configuration file' when I'm editing a JavaScript file.

If you're using SublimeLinter 4, the linter is trying to always lint the current view, even if there's no ESLint setup for the project or file. You can easily fix this error by creating an empty `.eslintrc` file in your home directory. This file will be picked up by the linter when there is **no** locally-defined ESLint configuration.

Use your editor of choice and create this config file, or do this on a terminal:

```bash
cd $HOME # or cd %HOMEPATH% on Windows
touch .eslintrc
echo '{ "rules": {} }' > .eslintrc
```

### I use `eslint_d` and the linter suddently stopped working

If you use `eslint_d` and the linter suddently stopped working with an error message like "Error: ENOENT: no such file or directory, open /../eslint/node_modules/globals/index.js", a restart of `eslint_d` might resolve the problem:

```bash
eslint_d restart
```
