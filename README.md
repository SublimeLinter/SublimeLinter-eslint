SublimeLinter-eslint
=========================

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [ESLint](https://github.com/nzakas/eslint).
It will be used with files that have the "javascript" syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. 

Please install via [Package Control](https://packagecontrol.io).

Before using this plugin, ensure that `eslint` is installed on your system.
To install `eslint`, do the following:

- Install [Node.js](http://nodejs.org) (and [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) on Linux).

- Install `eslint` globally by typing the following in a terminal:
```
npm install -g eslint
```
    
- Or install `eslint` locally in your project folder (**you must have package.json file there**):
```
npm install eslint
```

## Using eslint with plugins (e.g. vue)

If you're using plugins for eslint so that it can lint files other than `.js`, 
you need to tell SublimeLinter it's ok to lint those files too.
For this you can change the `"selector"` setting to include the scope
of the other syntax. For [vue](https://vuejs.org) this would be:

```json
"linters": {
    "eslint": {
        "selector": "text.html.vue, source.js - meta.attribute-with-value"
    }
}
```

## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

You can configure `eslint` options in the way you would from the command line, with `.eslintrc` files. For more information, see the [eslint docs](https://github.com/nzakas/eslint/wiki).


## FAQ and Troubleshooting

### I've got 'SublimeLinter: ERROR: eslint cannot locate 'eslint' in ST console when I try to use locally installed `eslint`.

You **must** have `package.json` file if install `eslint` locally. Also, restart project or ST itself after to make sure SublimeLinter uses correct `eslint` instance.

```
npm init -f
npm install eslint
```

### I've got 'SublimeLinter: eslint ERROR: ESLint couldn't find a configuration file' when I am editing a Javascript file.

If using SublimeLinter 4, the linter is trying to always lint the current view, even if there is no eslint setup for the project or file. 
You can easily fix this error by creating an empty `.eslintrc` file in your home directory. This file will be picked up by the linter when there is **no** locally-defined ESLint configuration.

Use your editor of choice and create this config file, or do this on a terminal:

```bash
cd $HOME # or cd %HOMEPATH% on Windows
touch .eslintrc
echo '{ "rules": {} }' > .eslintrc
```
