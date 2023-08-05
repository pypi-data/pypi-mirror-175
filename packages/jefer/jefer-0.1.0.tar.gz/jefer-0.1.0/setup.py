# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jefer']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['jefer = jefer.main:app']}

setup_kwargs = {
    'name': 'jefer',
    'version': '0.1.0',
    'description': 'A simple dotfiles manager written in asynchronous Python code.',
    'long_description': '# Jefer: A Simple Dotfiles Manager\n\nJefer is a **VERY** simple (with <200 lines of code!) dotfiles management tool\nwritten in Python.\n\nIf you Google for dotfiles manager, you will stumble upon a countless\nalternatives. And each one of those tools are very good due to their\nmaturity & the community support. You can read more of such alternatives in the\nproject documentation -\n"[https://jefer.vercel.app/about-the-project/alternatives-to-jefer][1]"\n\nAnd when compared to the existing alternatives, Jefer provides:\n\n1. True cross-platform support thanks to Python (but support for Windows is not\n   tested reliably).\n\n2. Hands-on configuration experience for your tools, Jefer stays away from how\n   you configure your tools. It only manages them in a version-control\n   environment.\n\n3. Offers a minimal & intuitive user-experience meaning, the user no longer has\n   to memorise way too many command-line options & flags.\n\n**NOTE**: Development on Jefer is still underway & its still a very\nwork-in-progress project, so expect things to break or behave in unintended\nways! If you come across such behaviour, please open an issue/discussion\nthread.\n\n## Usage Guidelines\n\nJefer will eventually be available on a lot other platforms like [Homebrew][2],\n[FlatHub][3] & more but for now it\'s only available through [PyPi][4]. If you\nwant Jefer to be available on more platforms, then please refer to the docs on\n"[_Distribution & Release Guidelines][5]" section before opening a discussion\nthread and/or a pull request.\n\nThat said, here\'s how you can install Jefer right now:\n\n```console\npipx install jefer\n```\n\nFor those of you who\'re not aware, [`pipx`][6] is the recommended way to install\nPython-based CLI tools.\n\n## Usage Terms & Conditions\n\nThe project is licensed under the terms & conditions of the MIT License. Hence\nyou\'re free to modify, copy, redistribute & use the project for commercial\npurposes as long as you adhere to the terms & conditions of the license.\n\nFor more information on the licensing details, check out the [LICENSE][1]\ndocument.\n\nInterested in contributing to the project? Check out the contribution guidelines\nthen.\n\n<!-- Reference Links -->\n\n[1]: https://jefer.vercel.app/about-the-project/alternatives-to-jefer\n[2]: https://brew.sh\n[3]: https://flathub.org\n[4]: https://pypi.org\n[5]: https://jefer.vercel.app/contributing-to-the-project/distribution-and-release-guidelines\n[6]: https://pypa.github.io/pipx\n[7]: ./LICENSE\n',
    'author': 'Somraj Saha',
    'author_email': 'somraj.mle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
