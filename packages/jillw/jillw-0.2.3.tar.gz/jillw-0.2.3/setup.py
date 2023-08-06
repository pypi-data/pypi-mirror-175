# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jillw']

package_data = \
{'': ['*']}

install_requires = \
['jill>=0.11.1,<0.12.0', 'tomli>=2.0.1,<3.0.0', 'wisepy2>=1.3,<2.0']

entry_points = \
{'console_scripts': ['jillw = jillw.cli:main', 'julia = jillw.cli:julia']}

setup_kwargs = {
    'name': 'jillw',
    'version': '0.2.3',
    'description': 'The wrapper for jill.py and manage Julia environments with Python virtualenv',
    'long_description': '# JILL Wrapper\n\nJILL Wrapper (`jillw`) is a lightweight and cross-platform Julia version manager. This work is based on [johnnychen94/jill.py](https://github.com/johnnychen94/jill.py) and [Python venv](https://docs.python.org/3/library/venv.html).\n\n`jillw` targets several different use cases:\n\n1. cross-platform julia installation\n2. cross-platform julia version management (create, switch, remove, etc.)\n3. providing the "one Julia, one Python" installation\n\n## Installation\n\n```bash\npip install -U jillw\n```\n\n## Usage\n\n### Create environments\n\n```shell\n> jillw create --help\nusage: create [-h] [--name NAME] [--upstream UPSTREAM] [--version VERSION] [--confirm] [--unstable] [name] [upstream] [version]\n\n# create a new environment using Julia 1.8\n> jillw create myenv --version 1.8\n```\n\nThe explanations of the arguments except `name` are referred to [johnnychen94/jill.py](https://github.com/johnnychen94/jill.py).\n\n### Activate environments\n\n```shell\n> jillw switch <envname>\n\n> jillw switch myenv\n```\n\n### Start `julia` under environments\n\n```shell\n> jillw switch myenv\n> julia --compile=min --quiet\njulia> Sys.which("julia")\n"~/.jlenvs/myenv/julia/julia-1.8/bin/julia.exe"\n```\n\n### List environments\n\n```shell\n> jillw list\nmyenv => ~/.jlenvs/myenv\nlatest => ~/.jlenvs/latest\n```\n\n### Remove environments\n\n```shell\n> jillw remove latest\nEnvironment latest removed.\n```\n\n### Run commands under environments\n\n```shell\n> jillw switch myenv\n> jillw run \'echo %VIRTUAL_ENV%\'\n~/.jlenvs/myenv\n```\n\n\n### Configuring the `julia` command (Experimental)\n\nBy creating a `Development.toml` at a working directory, you can conveniently configure the `julia` command to have the following features:\n\n- reduce the startup time by using interpreted mode\n- activate a project on startup\n- preload some specified files on startup\n- preload some modules on startup\n\nUse `jillw devhere` to create a template `Development.toml` at the current working directory.\n\nThe following options can be modified to fit your needs:\n\n- `min-latency`: a boolean that tells whether to use interpreted mode. This makes Julia code slow, but much faster at Julia startup and first-time module loading.\n\n- `no-startup-file`: a boolean that tells whether to load the `~/.julia/config/startup.jl` file.\n\n- `project`: a string thats indicates the path to the project that is expected to be activated on startup.\n\n- `sysimage`: a string thats indicates the path to the sysimage that is expected to be used on startup.\n\n- `using`: a list of strings that indicates the modules that are expected to be preloaded on startup.\n\n- `files`: a list of strings that indicates the files that are expected to be preloaded on startup.\n\n## License\n\nSee [LICENSE.md](./LICENSE.md).\n',
    'author': 'Suzhou-tongyuan',
    'author_email': 'support@tongyuan.cc',
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
