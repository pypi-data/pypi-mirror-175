# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flakeheaven',
 'flakeheaven._logic',
 'flakeheaven._patched',
 'flakeheaven.commands',
 'flakeheaven.formatters',
 'flakeheaven.parsers',
 'flakeheaven.plugins']

package_data = \
{'': ['*']}

install_requires = \
['colorama',
 'entrypoints',
 'flake8>=4.0.1,<5.0.0',
 'pygments',
 'toml',
 'urllib3']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0'],
 'docs': ['alabaster',
          'pygments-github-lexers',
          'sphinx',
          'myst-parser>=0.18.0,<0.19.0']}

entry_points = \
{'console_scripts': ['flake8heavened = flakeheaven:flake8_entrypoint',
                     'flakeheaven = flakeheaven:entrypoint'],
 'flake8.extension': ['pylint = flakeheaven.plugins:PyLintChecker'],
 'flake8.report': ['baseline = flakeheaven.formatters:BaseLineFormatter',
                   'colored = flakeheaven.formatters:ColoredFormatter',
                   'gitlab = flakeheaven.formatters:GitlabFormatter',
                   'grouped = flakeheaven.formatters:GroupedFormatter',
                   'json = flakeheaven.formatters:JSONFormatter',
                   'stat = flakeheaven.formatters:StatFormatter']}

setup_kwargs = {
    'name': 'flakeheaven',
    'version': '3.2.1',
    'description': 'FlakeHeaven is a [Flake8](https://gitlab.com/pycqa/flake8) wrapper to make it cool.',
    'long_description': '# FlakeHeaven\n\n[![License: MIT](https://img.shields.io/pypi/l/flakeheaven)](https://opensource.org/licenses/MIT)\n[![python versions](https://img.shields.io/pypi/pyversions/flakeheaven)](https://pypi.org/project/flakeheaven/)\n\n[![version](https://img.shields.io/pypi/v/flakeheaven)](https://pypi.org/project/flakeheaven/)\n[![conda](https://anaconda.org/conda-forge/flakeheaven/badges/version.svg)](https://anaconda.org/conda-forge/flakeheaven)\n[![Downloads](https://img.shields.io/pypi/dm/flakeheaven)](https://pypi.org/project/flakeheaven/)\n\n[![CI](https://github.com/flakeheaven/flakeheaven/actions/workflows/ci.yaml/badge.svg)](https://github.com/flakeheaven/flakeheaven/actions/workflows/ci.yaml)\n[![Docs](https://readthedocs.org/projects/flakeheaven/badge/?version=latest)](https://flakeheaven.readthedocs.io/en/latest/)\n\n\nflakeheaven is a python linter built around flake8 to enable inheritable and complex toml configuration.\n\nThis project is a fork of [FlakeHell](https://github.com/life4/flakehell). FlakeHell and other forks of it such as\nflakehell/flakehell are [no longer maintained](https://github.com/flakehell/flakehell/issues/25) and do not work with Flake8 4.0.x.\n\nFlakeHeaven works with Flake8 4.0.1 or greater. This fork will be [maintained by the community](https://github.com/flakeheaven/flakeheaven/discussions/1) that developed the existing forks.\n\n+ [Lint md, rst, ipynb, and more](https://flakeheaven.readthedocs.io/en/latest/parsers.html).\n+ [Shareable and remote configs](https://flakeheaven.readthedocs.io/en/latest/config.html#base).\n+ [Legacy-friendly](https://flakeheaven.readthedocs.io/en/latest/commands/baseline.html): ability to get report only about new errors.\n+ Caching for much better performance.\n+ [Use only specified plugins](https://flakeheaven.readthedocs.io/en/latest/config.html#plugins), not everything installed.\n+ [Make output beautiful](https://flakeheaven.readthedocs.io/en/latest//formatters.html).\n+ [pyproject.toml](https://www.python.org/dev/peps/pep-0518/) support.\n+ [Check that all required plugins are installed](https://flakeheaven.readthedocs.io/en/latest/commands/missed.html).\n+ [Syntax highlighting in messages and code snippets](https://flakeheaven.readthedocs.io/en/latest/formatters.html#colored-with-source-code).\n+ [PyLint](https://github.com/PyCQA/pylint) integration.\n+ [Powerful GitLab support](https://flakeheaven.readthedocs.io/en/latest/formatters.html#gitlab).\n+ Codes management:\n    + Manage codes per plugin.\n    + Enable and disable plugins and codes by wildcard.\n    + [Show codes for installed plugins](https://flakeheaven.readthedocs.io/en/latest/commands/plugins.html).\n    + [Show all messages and codes for a plugin](https://flakeheaven.readthedocs.io/en/latest/commands/codes.html).\n    + Allow codes intersection for different plugins.\n\n![output example](./assets/grouped.png)\n\n## Compatibility\n\nFlakeHeaven supports all flake8 plugins, formatters, and configs. However, FlakeHeaven has it\'s own beautiful way to configure enabled plugins and codes. So, options like `--ignore` and `--select` unsupported. You can have flake8 and FlakeHeaven in one project if you want but enabled plugins should be explicitly specified.\n\n## Installation\n\n```bash\npython3 -m pip install --user flakeheaven\n```\n\n## Usage\n\nFirst of all, let\'s create `pyproject.toml` config:\n\n```toml\n[tool.flakeheaven]\n# optionally inherit from remote config (or local if you want)\nbase = "https://raw.githubusercontent.com/flakeheaven/flakeheaven/main/pyproject.toml"\n# specify any flake8 options. For example, exclude "example.py":\nexclude = ["example.py"]\n# make output nice\nformat = "grouped"\n# 80 chars aren\'t enough in 21 century\nmax_line_length = 90\n# show line of source code in output\nshow_source = true\n\n# list of plugins and rules for them\n[tool.flakeheaven.plugins]\n# include everything in pyflakes except F401\npyflakes = ["+*", "-F401"]\n# enable only codes from S100 to S199\nflake8-bandit = ["-*", "+S1??"]\n# enable everything that starts from `flake8-`\n"flake8-*" = ["+*"]\n# explicitly disable plugin\nflake8-docstrings = ["-*"]\n```\n\nShow plugins that aren\'t installed yet:\n\n```bash\nflakeheaven missed\n```\n\nShow installed plugins, used plugins, specified rules, codes prefixes:\n\n```bash\nflakeheaven plugins\n```\n\n![plugins command output](./assets/plugins.png)\n\nShow codes and messages for a specific plugin:\n\n```bash\nflakeheaven codes pyflakes\n```\n\n![codes command output](./assets/codes.png)\n\nRun flake8 against the code:\n\n```bash\nflakeheaven lint\n```\n\nThis command accepts all the same arguments as Flake8.\n\nRead [the documentation](https://flakeheaven.readthedocs.io/en/latest/) for more information.\n\n## Contributing\n\n1. Add tests when possible (eg for features / fixes / refactor, etc. )\n2. add your contribution to the code / docs\n3. Ensure your code passes all (both oririnal and your own) tests.\n4. commit using [proper header](https://www.conventionalcommits.org/en/v1.0.0/)\n5. create a PR\n\nContributions are welcome! A few ideas where you can contribute:\n\n+ Improve documentation.\n+ Add more tests.\n+ Improve performance.\n+ Found a bug? Fix it!\n+ Made an article about FlakeHeaven? Great! Let\'s add it into the `README.md`.\n+ Don\'t have time to code? No worries! Just tell your friends and subscribers about the project. More users -> more contributors -> more cool features.\n\nA convenient way to run tests is using [Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer):\n\n```bash\ncurl -sSL https://install.python-poetry.org | python3 -\npoetry install\npoetry run pytest tests\n```\n\nThank you :heart:\n\n![](./assets/flaky.png)\n\nThe FlakeHeaven mascot (Flaky) is created by [@illustrator.way](https://www.instagram.com/illustrator.way/) and licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.\n',
    'author': 'Gram',
    'author_email': 'master_fess@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/flakeheaven/flakeheaven',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
