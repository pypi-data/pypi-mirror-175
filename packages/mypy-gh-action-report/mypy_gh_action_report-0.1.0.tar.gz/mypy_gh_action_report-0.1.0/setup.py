# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypy_gh_action_report']

package_data = \
{'': ['*']}

install_requires = \
['actions-toolkit>=0.1.15,<0.2.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['mypy-gh-action-report = '
                     'mypy_gh_action_report.main:execute']}

setup_kwargs = {
    'name': 'mypy-gh-action-report',
    'version': '0.1.0',
    'description': 'Notify Mypy output via GitHub Workflow Commands',
    'long_description': '[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mypy-gh-action-report.svg)](https://pypi.python.org/pypi/mypy-gh-action-report/)\n\n# mypy-gh-action-report\n\nNotify Mypy output via [GitHub Workflow Commands](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions)\n\n## Installation\n\n```bash\npip install mypy-gh-action-report\n```\n\n## Usage\n\n\n```bash\nmypy . | mypy-gh-action-report\n```\n\nor, to generate JSON output\n\n```bash\nmypy . | mypy-gh-action-report --json-only\n```\n\n## Output\n\nFor the following Mypy output:\n\n```bash\nmypy_gh_action_report/types.py:3: error: "list" expects 1 type argument, but 2 given  [type-arg]\nmypy_gh_action_report/models.py:13: error: Function is missing a return type annotation  [no-untyped-def]\nmypy_gh_action_report/parser.py:46: error: Item "None" of "Optional[MypyError]" has no attribute "file_name"  [union-attr]\nmypy_gh_action_report/parser.py:48: error: Item "None" of "Optional[MypyError]" has no attribute "line_no"  [union-attr]\nmypy_gh_action_report/main.py:16: error: Argument "mypy_output" to "handle_output" has incompatible type "Optional[str]"; expected "str"  [arg-type]\nFound 8 errors in 4 files (checked 7 source files)\n```\n\n`mypy-gh-action-report` will generate:\n\n```bash\n::warning title=,file=mypy_gh_action_report/types.py,line=3,endLine=,col=,endColumn=::"list" expects 1 type argument, but 2 given\n::warning title=,file=mypy_gh_action_report/models.py,line=13,endLine=,col=,endColumn=::Function is missing a return type annotation\n::warning title=,file=mypy_gh_action_report/parser.py,line=46,endLine=,col=,endColumn=::Item "None" of "Optional[MypyError]" has no attribute "file_name"\n::warning title=,file=mypy_gh_action_report/parser.py,line=48,endLine=,col=,endColumn=::Item "None" of "Optional[MypyError]" has no attribute "line_no"\n::warning title=,file=mypy_gh_action_report/main.py,line=16,endLine=,col=,endColumn=::Argument "mypy_output" to "handle_output" has incompatible type "Optional[str]"; expected "str"\n```\n\nwith `--json-only` flag:\n\n```json\n{\n  "mypy_gh_action_report/types.py": [\n    {\n      "line_no": 3,\n      "error_code": "type-arg",\n      "type": "error",\n      "message": "\\"list\\" expects 1 type argument, but 2 given"\n    }\n  ],\n  "mypy_gh_action_report/models.py": [\n    {\n      "line_no": 13,\n      "error_code": "no-untyped-def",\n      "type": "error",\n      "message": "Function is missing a return type annotation"\n    }\n  ],\n  "mypy_gh_action_report/parser.py": [\n    {\n      "line_no": 46,\n      "error_code": "union-attr",\n      "type": "error",\n      "message": "Item \\"None\\" of \\"Optional[MypyError]\\" has no attribute \\"file_name\\""\n    },\n    {\n      "line_no": 48,\n      "error_code": "union-attr",\n      "type": "error",\n      "message": "Item \\"None\\" of \\"Optional[MypyError]\\" has no attribute \\"line_no\\""\n    }\n  ],\n  "mypy_gh_action_report/main.py": [\n    {\n      "line_no": 16,\n      "error_code": "arg-type",\n      "type": "error",\n      "message": "Argument \\"mypy_output\\" to \\"handle_output\\" has incompatible type \\"Optional[str]\\"; expected \\"str\\""\n    }\n  ]\n}\n```\n\n## Development\n\nIn order to contribute to this project you need to have `poetry` installed.\n\nIn order to run tests issue:\n\n```bash\npoetry install\npoetry run pytest .\n```\n\n## Exit codes\n\nFollowing Scenarios are covered:\n\n| Description  | Mypy exit code | mypy-gh-action-report exit code |\n|--------------|----------|:--------------------------------|\n| Success      | 0 | 0                               |\n| Issues found | 1 | 1                               |\n| Mypy errors  | 2 | 2                               |\n\n## TODO\n\n1. Group warnings for the same line\n\n## Thanks\n\n- [actions-toolkit](https://github.com/yanglbme/actions-toolkit)\n- [typer](https://github.com/tiangolo/typer)',
    'author': 'Błażej Cyrzon',
    'author_email': 'blazej.cyrzon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
