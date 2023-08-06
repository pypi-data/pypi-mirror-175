# afam - ASC Files Analyzing Module

This package allows the user to analyze a ASC file, created by the EDF2ASC translator program of
SR Research. It converts selected events and samples from the EyeLink EDF file into
text, and sorts and formats the data into a form that is easier to work with.

It helps to perform the following operations:
 - Opening and closing the ASC file.
 - Matching words and messages to keywords (tokens).
 - Reading data items from the file, including recording start, button presses, eye events and
   messages and samples.

It contains the following event & sample classes:
 - **ASC_BUTTON** - a dataclass used to store the data from a "BUTTON" line
 - **ASC_EBLINK** - a dataclass used to store the data from an "EBLINK" line
 - **ASC_ESACC** - a dataclass used to store the data from an "ESACC" line
 - **ASC_EFIX** - a dataclass used to store the data from an "EFIX" line
 - **ASC_INPUT** - a dataclass used to store the data from a "INPUT" line
 - **ASC_MSG** - a dataclass used to store the data from a "MSG" line
 - **ASC_SBLINK** - a dataclass used to store the data from a "SBLINK" line
 - **ASC_SSACC** - a dataclass used to store the data from a "SSACC" line
 - **ASC_SFIX** - a dataclass used to store the data from a "SFIX" line
 - **ASC_MONO** - a dataclass used to store the data from a monocular "SAMPLE" line
 - **ASC_BINO** - a dataclass used to store the data from a binocular "SAMPLE" line

## Installation

```bash
$ pip install afam
```

## Usage

```python
import afam

dataset = afam.read_asc(file_name)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`afam` was created by Christoph Anzengruber. It is licensed under the terms of the GNU General Public License v3.0 license.

## Credits

`afam` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
