# Installation 
## Preliminaries
### Linux (Debian / Ubuntu)

Depending on your preferences, you may install the dependencies through APT, or through PIP. Please see the following steps if you want to use APT dependencies.

* Install `poetry`:

```bash
sudo apt update
sudo apt update python3-poetry
```

* Install the APT dependencies:

```bash
sudo apt install graphviz python3 python3-pylint
```

* If you are a developer, please also install the following dependencies:

```bash
sudo apt install git python3-pip bumpversion python3-coverage python3-pytest python3-pytest-cov python3-pytest-runner python3-sphinx python-pydata-sphinx-theme-doc
sudo pip3 install sphinx_mdinclude --break-system-packages
```

### Windows

* Install [poetry](https://pypi.org/project/poetry/).
* Install [graphviz](https://jupyter.org/install).

## Installing `fuzzy-set`
### From PIP

There are several ways to install the package:

* _System-wide:_ A modern ``pip3`` version prevents to install packages
system-wide. You must either use a virtual environment, or either pass the
`--break-system-packages` options:

```
sudo pip install fuzzy-set --break-system-packages
```

* _User-wide:_ As a normal user run:

```
pip install fuzzy-set --break-system-packages
```

* In a `poetry` environment: the package is available from program run using `poetry run ...`.

```bash
poetry run pip install
pip install fuzzy-set 
```

* In a
[virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):
the package is available only if this virtual environment is enabled.

```bash
python3 -m venv env      # Create your virtual environment
source env/bin/activate  # Activate the "env" virtual environment
which python             # Check you use the venv python interpret (i.e., not /usr/bin/python3)
pip install fuzzy-set 
deactivate               # Leave the  "env" virtual environment
```

### From git

* Clone the repository and install the package:

```bash
git clone https://github.com/Nokia-Bell-Labs/fuzzy-set.git
cd fuzzy-set 
```

* Install the missing dependencies and build the wheel of the project in a `poetry` environment:
```
poetry install  # Install the core dependencies. Pass --with docs,test,dev to install additional dependencies.
poetry build    # Build the wheel (see dist/*whl)
```

* The resulting `dist/fuzzy-set*whl` file can be installed using `pip` (see the previous section).

_Example:_ 

```bash
pip3 install dist/fuzzy-set*whl --break-system-packages 
```
