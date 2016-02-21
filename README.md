SublimeLinter-eslint
=========================

这个校验工具为 [SublimeLinter][docs] 提供 [ESLint](https://github.com/nzakas/eslint)接口. 它为带有“javascript”语法的文件提供帮助。

## 安装
SublimeLinter 3 必须安装. 如果 SublimeLinter 3 没有安装，请参考如下指导 [here][installation].

### 校验器 安装
使用本插件前, 你必须保证`eslint` 已经安装在你洗头.安装 `eslint`流程:

1. 安装 [Node.js](http://nodejs.org) (和 [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) on Linux).

1. 在终端全局安装 `eslint` :
   ```
   npm install -g eslint
   ```
或，在你项目路径，局部安装 `eslint`  (**you must have package.json file there**):
    ```
    npm init -f
    npm install eslint
    ```

接着重新打开你的项目 (或 重启 ST) 保证 `eslint` 可以使用.

1. 如果你使用 `nvm` 和 `zsh`, 保证在`.zprofile`加载 `nvm` ，而非 `.zshrc`.

1. 如果你使用 `zsh` 和 `oh-my-zsh`,别为 `oh-my-zsh`加载`nvm` 插件.

一旦 `eslint` 安装, 必须保证它在系统路径，让 SublimeLinter可以找到它. 这可能不会是你所想的理所当然, 请阅读 [how linter executables are located][locating-executables].

一旦你安装完 `eslint`，你可以进一步安装 SublimeLinter-eslint插件，如果你还没有安装的话.

**注意:** 本插件需要 `eslint` 0.20.0 或更高.

### 插件 安装
请使用 [Package Control][pc]安装校验插件. 这可以保证安装最新版本的插件. 如果你希望从源码安装，且做些修改,我想你可能知道怎么做，这里不多言.

通过 Package Control安装流程:

1. 在 Sublime Text, 启动 [Command Palette][cmd]，输入 `install`，将出现 `Package Control: Install Package`. 如果这个命令没有高亮，你可以用鼠标选择它. 这可能需要等待几秒钟，由 Package Control 获取可用的插件清单.

1. 当插件清单出现，输入 `eslint`. 你会看到 `SublimeLinter-contrib-eslint`.如果该选择没有高亮（选中），你可以用鼠标选择.

## 设置
关于SublimeLinter设置运行的一般信息, 参考 [设置][settings]. 有关校验设置的信息, 参考 [Linter Settings][linter-settings].

你可以配置 `eslint` 选项通过命令行, 使用 `.eslintrc` 文件.更多信息, 阅读 [eslint docs](https://github.com/nzakas/eslint/wiki).

## 问题

##### 我得到 'SublimeLinter: ERROR: eslint cannot locate 'eslint' in ST console ，当我尝试局部安装 `eslint`.

你 **必须** 存在 `package.json` 文件，如果局部安装 `eslint` . 另外,重启项目或 ST，保证使用正确的 `eslint` 实例.

```
npm init -f
npm install eslint
```

##### 插件仍然无法工作 或者 ST console出现错误.

升级 `eslint` 实例, 可能你使用了过期版本而 SublimeLinter 有时没有正确检查.

##### 我希望插件使用 `.eslintignore` 配置.

可以的.

##### 当 `.eslintrc` 文件不存在时，我希望不使用校验 (for ESLint <1.0.0).

使用 `--reset` [ESLint](http://eslint.org/docs/user-guide/command-line-interface#reset) 选项, 添加进你的 SublimeLinter 全局 配置 或 项目的 `.sublimelinterrc` 文件，如下. 添加 `--no-reset` 选项到项目 `.sublimelinterrc` 覆盖之.

```
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

##### 我希望使用全局的 `.eslintrc` 配置.

插件使用相同的[configuration hierarchy](http://eslint.org/docs/user-guide/configuring#configuration-cascading-and-hierarchy) as `eslint` 本身, 添加 `.eslintrc` 到你的根目录 或项目的祖先目录.

##### 我希望自定义规则, 全局 `.eslintignore` 文件, etc.

你可以订阅 **任何** [CLI options](http://eslint.org/docs/user-guide/command-line-interface#options) of `eslint` 带有 `args` key 在 SublimeLinter 配置中.

```
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

##### `context.getFilename()` 返回相对路径.

这是支持`.eslintignore` 配置的缺陷. 添加你的 SublimeLinter 配置:

```
{
    "linters": {
        "eslint": {
            "args": [
                "--stdin-filename", "@"
            ]
        }
    }
}
```

##### 插件不校验带有特殊符号的目录.

它看似 ST/SublimeLinter/ESLint 问题. 使用前述的方案, 设置 选项 `--stdin-filename` to `@`.

##### 不存在 `SublimeLinter-contrib-eslint` 包，在 使用 Package Control 安装时.

请检查你是否已经安装

## 贡献
如果你想修复或增强本项目, 请参考如下:

1. Fork 插件仓库.
1. 从最新的 `master`项目创建新的分支.
1. 提交合并分支.
1. 提出合并请求
1. 耐心等待.  ;-)

修改请遵循下面的代码指导:

- 4空格缩进.
- 代码通过 flake8 和 pep257 校验.
- 空行提高可阅读性, 请别担心使用它.
- 请使用描述性的变量名, 请别缩写，除非大家都知道.

感谢你的帮助!

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
[eslint_d]: https://github.com/mantoni/eslint_d.js
