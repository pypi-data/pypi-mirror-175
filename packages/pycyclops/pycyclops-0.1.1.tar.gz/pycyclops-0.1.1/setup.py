# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyclops',
 'cyclops.evaluation',
 'cyclops.evaluation.metrics',
 'cyclops.evaluation.metrics.functional',
 'cyclops.processors',
 'cyclops.processors.feature',
 'cyclops.query',
 'cyclops.query.postprocess',
 'cyclops.utils',
 'cyclops.workflow']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.5.3,<2.0.0',
 'Flask-Caching>=1.10.1,<2.0.0',
 'SQLAlchemy>=1.4.32,<2.0.0',
 'alibi-detect>=0.9.1,<0.10.0',
 'alibi>=0.6.5,<0.7.0',
 'black>=22.1.0,<23.0.0',
 'colorama>=0.4.4,<0.5.0',
 'dash-bootstrap-components>=1.1.0,<2.0.0',
 'dash-cool-components==0.1.8',
 'dash-iconify>=0.1.2,<0.2.0',
 'dash-mantine-components>=0.10.2,<0.11.0',
 'dash>=2.4.1,<3.0.0',
 'dask[dataframe]>=2022.9.1,<2023.0.0',
 'hydra-core>=1.2.0,<2.0.0',
 'llvmlite==0.38.0',
 'matplotlib>=3.5.1,<4.0.0',
 'nb-black>=1.0.7,<2.0.0',
 'numpydoc>=1.2,<2.0',
 'pandas>=1.4.1,<2.0.0',
 'plotly==5.7.0',
 'pre-commit>=2.17.0,<3.0.0',
 'prefect==2.0b6',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'pylint>=2.12.2,<3.0.0',
 'pyparsing==3.0.8',
 'pyproject-flake8==5.0.4',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=7.1.1,<8.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'seaborn>=0.11.2,<0.12.0',
 'shap>=0.40.0,<0.41.0',
 'tables>=3.7.0,<4.0.0',
 'torch>=1.11.0,<2.0.0',
 'torchxrayvision>=0.0.37,<0.0.38',
 'xgboost>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'pycyclops',
    'version': '0.1.1',
    'description': 'Framework for healthcare ML implementation',
    'long_description': "![cyclops Logo](https://github.com/VectorInstitute/cyclops/blob/main/docs/source/theme/static/cyclops_logo-dark.png?raw=true)\n\n--------------------------------------------------------------------------------\n\n[![Code checks](https://github.com/VectorInstitute/cyclops/actions/workflows/code_checks.yml/badge.svg)](https://github.com/VectorInstitute/cyclops/actions/workflows/code_checks.yml)\n[![Documentation and Coverage Report](https://github.com/VectorInstitute/cyclops/actions/workflows/docs_deploy.yml/badge.svg)](https://github.com/VectorInstitute/cyclops/actions/workflows/docs_deploy.yml)\n\n``cyclops`` is a framework for facilitating research and deployment of ML models\nin the health (or clinical) setting. It provides three high-level features:\n\n\n* Data Querying and Processing\n* Rigorous Evaluation\n* Drift Detection toolkit\n\n``cyclops`` also provides a library of use-cases on clinical datasets. The implemented\nuse-cases include:\n\n* Mortality decompensation prediction\n\n\n## 🐣 Getting Started\n\n### Setup Python virtual environment and install dependencies\n\nThe development environment has been tested on ``python = 3.9.7``.\n\nThe python virtual environment can be setup using\n[poetry](https://python-poetry.org/docs/#installation). Hence, make sure it is\ninstalled and then run:\n\n```bash\npoetry install\nsource $(poetry env info --path)/bin/activate\n```\n\n> ⚠️ ``poetry`` is the preferred installation method since it also installs\nthe ``cyclops`` package, and is tested. There is also an ``environment.yaml``\nand ``requirements.txt`` to install dependencies using\n[Miniconda](https://docs.conda.io/en/latest/miniconda.html) or\n[pip](https://pypi.org/project/pip/), however is not tested frequently.\n\n\n## 📚 [Documentation](https://vectorinstitute.github.io/cyclops/)\n\n## 🎓 Notebooks\n\nTo use jupyter notebooks, the python virtual environment can be installed and\nused inside an Ipython kernel. After activating the virtual environment, run:\n\n```bash\npython3 -m ipykernel install --user --name <name_of_kernel>\n```\n\nNow, you can navigate to the notebook's ``Kernel`` tab and set it as\n``<name_of_kernel>``.\n\nTutorial notebooks in ``tutorials`` can be useful to view the\nfunctionality of the framework.\n",
    'author': 'Vector AI Engineering',
    'author_email': 'cyclops@vectorinstitute.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VectorInstitute/cyclops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.9.7',
}


setup(**setup_kwargs)
