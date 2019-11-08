SublimeLinter-eslint
=========================

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [ESLint](https://github.com/nzakas/eslint). It will be used with files that have the "JavaScript" or "HTML 5" syntax dependent on your installed syntax highlighting package.

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
    
- Or install `eslint` locally in your project folder (**you must have a `package.json` file there**):
```
npm install eslint
```

## Using eslint with plugins (e.g. vue)

If you're using plugins for eslint so that it can lint files other than `.js`, 
you need to tell SublimeLinter it's ok to lint those files too.
For this you can change the `"selector"` setting to include the scope
of the other syntax. For [Vue.js](https://vuejs.org/) `.vue` files it would be:

```json
"linters": {
    "eslint": {
        "selector": "text.html.vue, source.js - meta.attribute-with-value"
    }
}
```

For [Svelte](https://svelte.dev/) `.svelte` files, using [`eslint-plugin-svelte3`](https://github.com/sveltejs/eslint-plugin-svelte3) and the [Naomi](https://packagecontrol.io/packages/Naomi) syntax highlighter set to HTML 5, it would be:

```json
"linters": {
    "eslint": {
        "selector": "text.html"
    }
}
```

To find the `selector` value for a particular file type, place the cursor at the start of the file and use the command **Tools** ➡️ **Developer** ➡️ **Show Scope Name**.

## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

You can configure `eslint` options in the way you would from the command line, with `.eslintrc` files. For more information, see the [eslint docs](https://github.com/nzakas/eslint/wiki).


## FAQ and Troubleshooting

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
