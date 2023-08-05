# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psimpy',
 'psimpy.emulator',
 'psimpy.inference',
 'psimpy.sampler',
 'psimpy.sensitivity',
 'psimpy.simulator',
 'psimpy.utility']

package_data = \
{'': ['*']}

install_requires = \
['SALib>=1.4.5,<2.0.0',
 'beartype>=0.11.0,<0.12.0',
 'numpy>=1.22.3,<2.0.0',
 'rpy2>=3.5.1,<4.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'psimpy',
    'version': '0.1.2',
    'description': 'Predictive and probabilistic simulation tools.',
    'long_description': '## Description\n\n`PSimPy` (Predictive and probabilistic simulation with Python) implements\na Gaussian process emulation-based framework that enables systematically and\nefficiently inverstigating uncertainties associated with physics-based models\n(i.e. simulators).\n\n## Installation\n\n`PSimPy` is a pure Python package and can be easily installed using `pip`. All\nPython-related dependencies are automatically taken care of. It should be noted\nthat some modules of `PSimPy` rely on / take advantage of non-Python package and\nsoftware. More specifically, the emulator module `robustgasp.py` relies on the R\npackage `RobustGaSP`; the simulator module `ravaflow24.py` relies on the open\nsource software `r.avaflow 2.4`. If you want to use these modules or any other\nmodules relying on these modules, corresponding non-Python dependencies need to\nbe installed.\n\nIf the simulator module `ravaflow.py` is desired, you may follow the official\ndocumentation of `r.avaflow 2.4` under https://www.landslidemodels.org/r.avaflow/\nto install it. The installation of the R package `RobustGaSP` is covered in\nfollowing steps.\n\nWe recommond you to install `PSimPy` in a virtual environment such as a `conda`\nenvironment. You may want to first install `Anaconda` or `Miniconda` if you\nhaven\'t. The steps afterwards are as follows:\n\n1. Create a conda environment with Python 3.9:\n\n```bash\nconda create --name your_env_name python=3.9\n```\n\n2. Install `R` if you don\'t have it on your machine (if you have `R`, you can\nskip this step; alternatively, you can still follow this step to install `R` in\nthe conda environment):\n```bash\nconda activate your_env_name\nconda install -c conda-forge r-base=3.6\n```\n\n3. Install the R package `RobustGaSP` in the R terminal:\n```bash\nR\ninstall.packages("RobustGaSP",repos="https://cran.r-project.org",version="0.6.4")\n```\nTry if it is successfully installed by\n```bash\nlibrary("RobustGaSP")\n```\n\n4. Configure the environment variable `R_HOME` so that `rpy2` knows where to find\n`R` packages. You can find your `R_HOME` by typing the following command in the\nR terminal:\n```bash\nR.home()\nq()\n```\nIt is a path like ".../lib/R". Set the environment variable `R_HOME` in your\nconda environment by\n```bash\nconda env config vars set R_HOME=your_R_HOME\n```\nAfterwards reactivate your conda environment to make the change take effect by\n```bash\nconda deactivate\nconda activate your_env_name\n```\n\n5. Install `PSimPy` using `pip` in your conda environment by\n```bash\nconda install -c conda-forge pip\npip install psimpy\n```\n\nNow you should have `PSimPy` and its dependencies successfully installed.\n\n## Usage\nExamples are currently in preparation and will be available soon in coming\nversions. You may want to have a look at the tests which are currently available\nat https://git-ce.rwth-aachen.de/mbd/psimpy. They give a glimpse of how `PSimpy`\ncan be used. You may download the `tests` folder onto your local machine, and run\nany test using `pytest`. \n\nFirst install `pytest` by\n```bash\nconda activate your_env_name\nconda install pytest\n```\nThen navigate to the folder where `tests` folder is located on your machine.\nYou may run all the tests by\n```bash\npytest tests/\n```\nor a specific test like `test_active_learning` by\n```bash\npytest tests/test_active_learning.py\n```\nSome tests save results including plots into temporary folders. The temporary\nfolders will be deleted automatically if `test_clear_temp_file` is called. If\nyou want to exclude a specific test such as `test_clear_temp_file`, you may run\n```bash\npytest tests/ --ignore=tests/test_clear_temp_file.py\n```\n\n## Documentation\nThe source codes of `PSimPy` contains detailed docstrings which explain how it\ncan be used. More documentation about the theories is currently in preparation\nand will be available soon.\n\n## License\n\n`PSimPy` was created by Hu Zhao at the Chair of Methods for Model-based\nDevelopment in Computational Engineering. It is licensed under the terms of\nthe MIT license.',
    'author': 'Hu Zhao',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git-ce.rwth-aachen.de/mbd/psimpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
