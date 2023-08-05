# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretext', 'pretext.core', 'pretext.templates', 'pretext.templates.resources']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3,<4',
 'PyPDF2>=2.5,<2.6',
 'click-log>=0.4,<0.5',
 'click>=8,<9',
 'ghp-import>=2,<3',
 'lxml>=4.8,<5.0',
 'pdfCropMargins>=1.0.9,<1.1.0',
 'pyppeteer>=1.0.2,<2.0.0',
 'requests>=2,<3',
 'single-version>=1,<2',
 'watchdog>=2,<3']

entry_points = \
{'console_scripts': ['pretext = pretext.cli:main']}

setup_kwargs = {
    'name': 'pretext',
    'version': '1.0.6.dev20221103',
    'description': 'A package to author, build, and deploy PreTeXt projects.',
    'long_description': '# PreTeXt-CLI\n\nA package for authoring and building [PreTeXt](https://pretextbook.org) documents.\n\n- GitHub: <https://github.com/PreTeXtBook/pretext-cli/>\n\n## Documentation and examples for authors/publishers\n\nMost documentation for PreTeXt authors and publishers is available at:\n\n- <https://pretextbook.org/doc/guide/html/>\n\nAuthors and publishers may also find the examples catalog useful as well:\n\n- <https://pretextbook.org/examples.html>\n\nWe have a few notes below (TODO: publish these in the Guide).\n\n### Installation\n\n#### Installing Python\n\nPreTeXt-CLI requires the Python version specified in `pyproject.toml`.\n\nTo check your version, type this into your terminal or command prompt:\n\n```\npython -V\n```\n\nIf your version is 2.x, try this instead\n(and if so, either replace all future references to `python`\nin these instructions with `python3`).\n\n```\npython3 -V\n```\n\nIf you don\'t have a compatible Python available, try one of these:\n\n- https://www.python.org/downloads/\n  - Windows warning: Be sure to select the option adding Python to your Path.\n- https://github.com/pyenv/pyenv#installation (Mac/Linux)\n- https://github.com/pyenv-win/pyenv-win#installation (Windows)\n\n#### Installing PreTeXt-CLI\n\nOnce you\'ve confirmed that you\'re using a valid version of Python, just\nrun (replacing `python` with `python3` if necessary):\n\n```\npython -m pip install --user pretext\n```\n\n(It\'s also possible you may get an error like \n`error: invalid command \'bdist_wheel\'`\n— good news, you can ignore it!)\n\nAfter installation, try to run:\n\n```\npretext --help\n```\n\nIf that works, great! Otherwise, it likely means that Python packages\naren\'t available on your “PATH”. In that case, replace all `pretext`\ncommands with `python -m pretext` instead:\n\n```\npython -m pretext --help\n```\n\nEither way, you\'re now ready to use the CLI, the `--help` option will explain how to use all the different\nsubcommands like `pretext new` and `pretext build`.\n\n#### External dependencies\n\nWe install as much as we can with the `pip install` command, but depending on your machine\nyou may require some extra software:\n\n- [TeXLive](https://www.tug.org/texlive/)\n- [pdftoppm/Ghostscript](https://github.com/abarker/pdfCropMargins/blob/master/doc/installing_pdftoppm_and_ghostscript.rst)\n\n#### Upgrading PreTeXt-CLI\nIf you have an existing installation and you want to upgrade to a more recent version, you can run:\n\n```\npython -m pip install --upgrade pretext\n```\n\n#### Custom XSL\n\nCustom XSL is not encouraged for most authors, but (for example) developers working\nbleeding-edge XSL from core PreTeXt may want to call XSL different from that\nwhich is shipped with a fixed version of the CLI. This may be accomplished by\nadding an `<xsl/>` element to your target with a relative (to `project.ptx`) or\nabsolute path to the desired XSL. *(Note: this XSL must only import\nother XSL files in the same directory or within subdirectories.)*\n\nFor example:\n\n```\n<target name="html">\n  <format>html</format>\n  <source>source/main.ptx</source>\n  <publication>publication/publication.ptx</publication>\n  <output-dir>output/html</output-dir>\n  <xsl>../pretext/xsl/pretext-html.xsl</xsl>\n</target>\n```\n\nIf your custom XSL file needs to import the XSL\nshipped with the CLI (e.g. `pretext-common.xsl`), then use a `./core/`\nprefix in your custom XSL\'s `xsl:import@href` as follows:\n\n```\n<xsl:import href="./core/pretext-common.xsl"/>\n```\n\nSimilarly, `entities.ent` may be used:\n\n```\n<!DOCTYPE xsl:stylesheet [\n    <!ENTITY % entities SYSTEM "./core/entities.ent">\n    %entities;\n]>\n```\n\n*Note: previously this was achieved with a `pretext-href` attribute - this is now deprecated and will be removed in a future release.*\n\n---\n\n## Development\n**Note.** The remainder of this documentation is intended only for those interested\nin contributing to the developement of this project.  Anyone who simply wishes to\n*use* the PreTeXt-CLI can stop reading here. \n\nFrom the "Clone or Download" button on GitHub, copy the `REPO_URL` into the below\ncommand to clone the project.\n\n```bash\ngit clone [REPO_URL]\ncd pretext-cli\n```\n\n### Using a valid Python installation\n\nDevelopers and contributors must install a\nversion of Python that matching the requirements in `pyproject.toml`.\n\n#### Using pyenv and poetry (Mac/Linux)\n\nThe `pyenv` tool for Linux automates the process of running the correct\nversion of Python when working on this project (even if you have\nother versions of Python installed on your system).\n\n- https://github.com/pyenv/pyenv#installation\n\nRun the following, replacing `PYTHON_VERSION` with your desired version.\n\n```\npyenv install PYTHON_VERSION\n```\n\nThen follow these instructions to install `poetry`.\n\n- https://python-poetry.org/docs/#installation\n    - Note 2022/06/21: you may ignore "This installer is deprecated". See\n      [python-poetry/poetry/issues/4128](https://github.com/python-poetry/poetry/issues/4128)\n\nThen you should be able to install dependencies into a virtual environment\nwith this command.\n\n```\npoetry install\n```\n\nThen to use the in-development package, you can either enter a poetry shell:\n\n```\npretext --version # returns system version\npoetry shell\npretext --version # returns version being developed\nexit\npretext --version # returns system version\n```\n\nOr use the runner (as long as you remain within the package directory):\n\n```\npretext --version             # returns system version\npoetry run pretext --version  # returns version being developed\n```\n\nIf you run `echo \'alias pr="poetry run"\' >> ~/.bashrc` then restart your\nshell, this becomes less of a mouthful:\n\n```\npretext --version     # returns system version\npr pretext --version  # returns version being developed\n```\n\n#### Steps on Windows\n\nIn windows, you can either use the bash shell and follow the directions above,\nor try [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation).  In\nthe latter case, make sure to follow all the installation instructions, including\nthe **Finish the installation**.  Then proceed to follow the directions above to\ninstall a version of python matching `.pyproject.toml`.  Finally, you may then need\nto manually add that version of python to your path.\n\n### Updating dependencies\n\nTo add dependencies for the package, run\n\n```\npoetry add DEPENDENCY-NAME\n```\n\nIf someone else has added a dependency:\n\n```\npoetry install\n```\n\n### Syncing untracked updates\n\nUpdates to certain files tracked to the repository will\nneed to be rebuilt by each user when pulled from GitHub.\n\nThe file `pretext/__init__.py` tracks the upstream\ncommit of core PreTeXt XSL/Python code we\'re developing against\n(from `PreTeXtBook/pretext`).\nTo fetch these updates from upstream, run:\n\n```\npoetry run python scripts/fetch_core.py\n```\n\nIf you instead want to point to a local copy of `PreTeXtBook/pretext`,\ntry this instead to set up symlinks:\n\n```\npoetry run python scripts/symlink_core.py path/to/pretext\n```\n\nUpdates to `templates/` must be zipped and moved into\n`pretext/templates/resources`. This is done automatically by\nrunning:\n\n```\npoetry run python scripts/zip_templates.py\n```\n\n### Testing\n\nSets are contained in `tests/`. To run all tests:\n\n```\npoetry run pytest\n```\n\nTo run a specific test, say `test_name` inside `test_file.py`:\n\n```\npoetry run pytest -k name\n```\n\nTests are automatically run by GitHub Actions when pushing to identify\nregressions.\n\n### Packaging\n\nTo check if a successful build is possible:\n\n```\npoetry run python scripts/build_package.py\n```\n\nTo publish a new alpha release, first add/commit any changes. Then\nthe following handles bumping versions, publishing to PyPI,\nand associated Git management.\n\n```\npoetry run python scripts/release_alpha.py\n```\n\nPublishing a stable release is similar:\n\n```\npoetry run python scripts/release_stable.py # patch +0.+0.+1\npoetry run python scripts/release_stable.py minor # +0.+1.0\npoetry run python scripts/release_stable.py major # +1.0.0\n```\n\n---\n\n## About\n\n### PreTeXt-CLI Lead Developers\n- [Steven Clontz](https://clontz.org/)\n- [Oscar Levin](https://math.oscarlevin.com/)\n\n### A note and special thanks\n\nA `pretext` package unrelated to the PreTeXtBook.org project was released on PyPI\nseveral years ago by Alex Willmer. We are grateful for his willingness to transfer\nthis namespace to us.\n\nAs such, versions of this project before 1.0 are released on PyPI under the\nname `pretextbook`, while versions 1.0 and later are released as `pretext`.\n\n### About PreTeXt\nThe development of [PreTeXt\'s core](https://github.com/PreTeXtBook/pretext)\nis led by [Rob Beezer](http://buzzard.ups.edu/).\n',
    'author': 'Steven Clontz',
    'author_email': 'steven.clontz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pretextbook.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
