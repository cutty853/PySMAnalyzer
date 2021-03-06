# PySMAnalyzer
[![Build Status](https://travis-ci.org/cutty853/PySMAnalyzer.png?branch=master)](https://travis-ci.org/cutty853/PySMAnalyzer)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/cutty853/PySMAnalyzer)
[![Coverage Status](https://coveralls.io/repos/github/cutty853/PySMAnalyzer/badge.svg?branch=master)](https://coveralls.io/github/cutty853/PySMAnalyzer?branch=master)

source-monitor analyzer for C code quality. Read XML source-monitor's report and create output report by extracting what matters.

## Usage
To use the program you must provide a source monitor report file (generated by using [Source Monitor][http://www.campwoodsw.com/sourcemonitor.html]) and a rules file created by ... [you][doc/rules_creation.md]. The rules file is made so that you can define the metrics you consider bad.

Here is the help page
```sh
>>> python main.py -h
usage: main.py [-h] [-t] [-o OUTPUT] [-f FORMAT] [input] [rules]

positional arguments:
  input                 source monitor input file
  rules                 rules file

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            Start all the unit-test of the project
  -o OUTPUT, --output OUTPUT
                        The output file
  -f FORMAT, --fomat FORMAT
                        output format, default: html
```

## Documentation
A [documentation for the project][doc/summary.md] is being written.

## Contributing
I don't have contribution policy yet, but you can open an issue if you want to see a new feature.
