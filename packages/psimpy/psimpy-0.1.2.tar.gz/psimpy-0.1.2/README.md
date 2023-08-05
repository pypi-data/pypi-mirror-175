## Description

`PSimPy` (Predictive and probabilistic simulation with Python) implements
a Gaussian process emulation-based framework that enables systematically and
efficiently inverstigating uncertainties associated with physics-based models
(i.e. simulators).

## Installation

`PSimPy` is a pure Python package and can be easily installed using `pip`. All
Python-related dependencies are automatically taken care of. It should be noted
that some modules of `PSimPy` rely on / take advantage of non-Python package and
software. More specifically, the emulator module `robustgasp.py` relies on the R
package `RobustGaSP`; the simulator module `ravaflow24.py` relies on the open
source software `r.avaflow 2.4`. If you want to use these modules or any other
modules relying on these modules, corresponding non-Python dependencies need to
be installed.

If the simulator module `ravaflow.py` is desired, you may follow the official
documentation of `r.avaflow 2.4` under https://www.landslidemodels.org/r.avaflow/
to install it. The installation of the R package `RobustGaSP` is covered in
following steps.

We recommond you to install `PSimPy` in a virtual environment such as a `conda`
environment. You may want to first install `Anaconda` or `Miniconda` if you
haven't. The steps afterwards are as follows:

1. Create a conda environment with Python 3.9:

```bash
conda create --name your_env_name python=3.9
```

2. Install `R` if you don't have it on your machine (if you have `R`, you can
skip this step; alternatively, you can still follow this step to install `R` in
the conda environment):
```bash
conda activate your_env_name
conda install -c conda-forge r-base=3.6
```

3. Install the R package `RobustGaSP` in the R terminal:
```bash
R
install.packages("RobustGaSP",repos="https://cran.r-project.org",version="0.6.4")
```
Try if it is successfully installed by
```bash
library("RobustGaSP")
```

4. Configure the environment variable `R_HOME` so that `rpy2` knows where to find
`R` packages. You can find your `R_HOME` by typing the following command in the
R terminal:
```bash
R.home()
q()
```
It is a path like ".../lib/R". Set the environment variable `R_HOME` in your
conda environment by
```bash
conda env config vars set R_HOME=your_R_HOME
```
Afterwards reactivate your conda environment to make the change take effect by
```bash
conda deactivate
conda activate your_env_name
```

5. Install `PSimPy` using `pip` in your conda environment by
```bash
conda install -c conda-forge pip
pip install psimpy
```

Now you should have `PSimPy` and its dependencies successfully installed.

## Usage
Examples are currently in preparation and will be available soon in coming
versions. You may want to have a look at the tests which are currently available
at https://git-ce.rwth-aachen.de/mbd/psimpy. They give a glimpse of how `PSimpy`
can be used. You may download the `tests` folder onto your local machine, and run
any test using `pytest`. 

First install `pytest` by
```bash
conda activate your_env_name
conda install pytest
```
Then navigate to the folder where `tests` folder is located on your machine.
You may run all the tests by
```bash
pytest tests/
```
or a specific test like `test_active_learning` by
```bash
pytest tests/test_active_learning.py
```
Some tests save results including plots into temporary folders. The temporary
folders will be deleted automatically if `test_clear_temp_file` is called. If
you want to exclude a specific test such as `test_clear_temp_file`, you may run
```bash
pytest tests/ --ignore=tests/test_clear_temp_file.py
```

## Documentation
The source codes of `PSimPy` contains detailed docstrings which explain how it
can be used. More documentation about the theories is currently in preparation
and will be available soon.

## License

`PSimPy` was created by Hu Zhao at the Chair of Methods for Model-based
Development in Computational Engineering. It is licensed under the terms of
the MIT license.