# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextcodecli',
 'nextcodecli.commands',
 'nextcodecli.commands.pipelines',
 'nextcodecli.commands.project',
 'nextcodecli.commands.query',
 'nextcodecli.commands.workflow',
 'nextcodecli.pipelines',
 'nextcodecli.workflow']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'hjson>=3.1.0,<4.0.0',
 'jsonpath-rw>=1.4.0,<2.0.0',
 'nextcode-sdk>=2.0.0,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['nextcode = nextcodecli.__main__:cli']}

setup_kwargs = {
    'name': 'nextcode-cli',
    'version': '3.0.0',
    'description': 'WuXi Nextcode commandline utilities',
    'long_description': '# NextCODE Command Line Interface\n\n- [Requirements](#requirements)\n- [Installation](#installation)\n  * [End-user installation](#end-user-installation)\n  * [Developer installation](#developer-installation)\n  * [Set up a service profile](#set-up-a-service-profile)\n    + [Create a service profile](#create-a-service-profile)\n    + [Running the CLI for the first time](#running-the-cli-for-the-first-time)\n- [Releasing](#releasing)\n\n# Requirements\n * Python 3.7\n\n# Installation\n\n## End-user installation\n\n**Prerequisites**\nNote that having `python3` (and a `pip3` that points to that python) is a prerequisite, the easist way to fullfil this is to install both via Homebrew.\n\nTo install the package you have to run the following command:\n```bash\n$ pip3 install nextcode-cli -U\n```\n\nTo verify that the installation was successful you can run the following command:\n```bash\n$ nextcode version\nnextcode-cli/x.y.z (yyyy.mm.dd)\n```\n\n## Developer installation\nStart by pulling the sourcecode from git (usually from develop to be on the bleeding edge).\n\nThere are two ways to set up the CLI. We recommend trying to install it into your system python in `develop` mode by simply running the following command in the nextcode-cli folder (depending on your system setup you might need `sudo`)\n```bash\n$ pip3 install -e .\n```\n\nIf you get any errors you can set up a local virtualenv in the nextcode-cli path:\n```bash\n$ source ./setup.sh\n$ pip3 install -e .\n```\nUsing this method means that you will always need to do `source ./setup.sh` to enter the virtualenv before using the tool, so we would recommend getting the first method to work unless you intend on make edits to the code yourself.\n\n## Set up a service profile\n### Create a service profile\nFor any work to happen a service profile must be defined. One example is the one here below, which is Platform Dev test specific. For QA purposes this is of course **test environment dependent**!:\n\nThe command is:\n```bash\n$ nextcode profile add <profile-name>\n```\n\nFollow the prompts to enter a server name and then log in through the browser window that opens up.\n\nYou can also set up the profile without a prompt like this:\n```bash\n$ nextcode profile add <profile-name> --domain=mydomain.wuxinextcode.com --api-key=<key>\n```\n\n### Running the CLI for the first time\n\nOnce your installation has succeeded you can run the following command anywhere in your system:\n```bash\nnextcode status\n```\nOnce you finish the authentication process you should be able to view workflow jobs:\n```bash\nnextcode workflow jobs\n```\n\nTo start familiarizing yourself with the sdk you can use the --help option on all commands to see detailed information about their use.\n```bash\n$ nextcode --help\nUsage: nextcode [OPTIONS] COMMAND [ARGS]...\n\n  A utility for interfacing with WuXi Nextcode services.\n\n  This tool allows you to communicate with the pipelines service, CSA,\n  workflow service and GOR Query API. For all usage you will need to\n  authenticate against the specific service profile you are using.\n\n  Please look at the subcommands below for details.\n\nOptions:\n  -v, --verbose [warning|error|info]\n                                  Output logs for debugging\n  -p, --profile TEXT              Use a specific profile for this command\n  --help                          Show this message and exit.\n\nCommands:\n  csa_authenticate  Authenticate against CSA (for import).\n  import            Import a TSV manifest into CSA.\n  keycloak          Manage keycloak users Requires the keycloak admin...\n  login             Authenticate against keycloak.\n  pipelines         Root subcommand for pipelines functionality\n  profile           Configure server profile to use.\n  query             Root subcommand for query api functionality\n  token             Print out an access token for the current profile\n  version           Show the Nextcode CLI version.\n  workflow          Root subcommand for workflow functionality\n\n$ nextcode workflow --help\nUsage: nextcode workflow [OPTIONS] COMMAND [ARGS]...\n\n  Root subcommand for workflow functionality\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  job        View or manage individual jobs.\n  jobs       List jobs\n  pipelines  List pipelines\n  projects   List projects\n  run        Start a new nextflow job.\n  smoketest  Run a smoketest of the workflow service\n  status     Show the status of the workflow service\n```\n\n# Releasing\n* Bump version and update the a date in [nextcodecli/VERSION](nextcodecli/VERSION)\n* Merge to master\n* Tag in Gitlab\n* Watch the CI fireworks. \n',
    'author': 'WUXI NextCODE',
    'author_email': 'support@wuxinextcode.com',
    'maintainer': 'Genuity Science Software Development',
    'maintainer_email': 'sdev@genuitysci.com',
    'url': 'https://www.wuxinextcode.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
