SDQC
====

This Python library allows checking the quality of the input data of [System Dynamics](http://en.wikipedia.org/wiki/System_dynamics) models developed in Vensim. It uses [PySD](https://github.com/SDXorg/pysd) library to parse the model and load the input data from spreadsheet files.

### Requirements

- Python 3.7+
- PySD 3.8+
- pypandoc (and pandoc 2.17+)
- netCDF4 (version 1.5 for Python 3.7 in Windows and 1.6+ for all other cases)
- importlib-metadata 2.0 (only required for Python 3.7)

### Resources
See the [project documentation](http://sdqc.readthedocs.org/) for information about:

- [Installation](http://sdqc.readthedocs.org/en/latest/installation.html)
- [Usage](http://sdqc.readthedocs.org/en/latest/usage.html)
- [Data quality reporting](http://sdqc.readthedocs.org/en/latest/report_configuration.html)

### Authority and acknowledgmentes
This library was developed by [@eneko.martin.martinez](https://gitlab.com/eneko.martin.martinez) at [Centre de Recerca Ecològica i Aplicacions Forestals (CREAF)](http://www.creaf.cat/).

This project has received funding from the European Union’s Horizon 2020
research and innovation programme under grant agreement No. 821105.
