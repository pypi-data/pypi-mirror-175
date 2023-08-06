# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['start_code']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.21,<0.22']

setup_kwargs = {
    'name': 'start-code',
    'version': '0.0.1',
    'description': 'Boilerplate Python Code',
    'long_description': '# Name of Project Title Here\n\nEnter brief description.\n\n## Gotchas\n\n- When `poetry update` fails, search for libraries.\n- Upgrade pip: `pip3 install -U pip` inside the .venv, i.e. in `poetry shell`\n- Use `pip3` instead of `poetry add` or `poetry update` when third-party library install fails, e.g. `pip3 install -U virtualenv`.\n\n## Quickstart\n\n### Copy from source\n\n1. `gh repo clone justmars/start_code` _target_\n2. Rename `start_code` folder to _target_ or delete\n3. Add `.vscode` to `.gitignore`\n\n### Set python version\n\n1. Check [.python-version](./.python-version), default is 3.10.7\n2. Run `poetry env use $(pyenv which python)` if `.python-version` has been updated. See [ticket](https://github.com/python-poetry/poetry/issues/651#issuecomment-1073213937)\n3. Review created .venv folder\'s `pyvenv.cfg` this should show the version declared in `.python-version`\n\n## Configure package\n\n1. Open [pyproject.toml](./pyproject.toml)\n2. Change `name` from `start_code` to `desired-package-name` (not a duplicate in pypi)\n3. Add description\n4. Remove dependencies that aren\'t applicable, e.g. `tqdm`\n5. Create the virtual environment via `poetry install`\n\n## Setup git repo\n\nNote: can avoid this section if not creating a repository\n\nWhile virtual environment being installed, create new repo. Get repo `<url>`\n\n```zsh\n> `rm -rf .git` # remove cloned .git file\n> `git init -b main`\n> `git add .`\n> `git commit -m "first"`\n> `git remote add origin` <url> # from created repo\n> `pre-commit run -a`\n> `git push -u origin main`\n```\n\n## Cleanup\n\n1. Add license, repository, packages to [pyproject.toml](./pyproject.toml), when ready.\n2. Delete contents of this README from `Gotchas` going down.\n3. Update precommit [config](./pre-commit-config.yaml) version numbers to match [pyproject.toml](./pyproject.toml), in case these have been updated.\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
