#!/usr/bin/env python

"""Mobile Balance.

Usage:
  mobile-balance <operator> --number=<phone-number> --password=<password>
  mobile-balance (-h | --help)
  mobile-balance --version

Options:
  -h --help                Show this screen.
  --version                Show version.
  --number=<phone-number>  Mobile number without 8 or +7 prefix.
  --password=<password>    Password from personal profile at mobile operator's site.

"""

from mobile_balance import mts
from docopt import docopt

OPERATORS = dict(
    mts=mts)

def main():
    arguments = docopt(__doc__, version='Mobile Balance 0.1.0')
    mobile_operator = OPERATORS[arguments['<operator>']]
    print mobile_operator.get_balance(arguments['--number'],
                                      arguments['--password'])
