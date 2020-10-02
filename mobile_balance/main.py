#!/usr/bin/env python

"""Mobile Balance.

Usage:
  mobile-balance <operator> --phone=<phone-number> --password=<password> [--bad-responses-dir=<bad-responses-dir]
  mobile-balance (-h | --help)
  mobile-balance --version

Options:
  -h --help                Show this screen.
  --version                Show version.
  --phone=<phone-number>  Mobile number without 8 or +7 prefix.
  --password=<password>    Password from personal profile at mobile operator's site.
  --bad-responses-dir=<bad-responses-dir> Directory to save bad responses to.

"""

import os
import sys
import time

from mobile_balance import mts, megafon, tele2, ttk, beeline, exceptions
from docopt import docopt
from pkg_resources import get_distribution


def main():
    arguments = docopt(__doc__, version='Mobile Balance %s'
                       % get_distribution('mobile_balance').version)
    operator_name = arguments['<operator>']
    mobile_operator = globals()[operator_name]
    try:
        print(mobile_operator.get_balance(arguments['--phone'],
                                          arguments['--password']))
    except exceptions.BadResponse as e:
        print(e, file=sys.stderr)
        bad_responses_dir = arguments['--bad-responses-dir']
        if bad_responses_dir:
            bad_responses_dir = os.path.join(bad_responses_dir,
                                             operator_name)
            if not os.path.exists(bad_responses_dir):
                os.makedirs(bad_responses_dir)

            filename = os.path.join(bad_responses_dir,
                                    '{0}-{1}.html'.format(
                                        e.response.status_code,
                                        time.time()))
            with open(filename, 'w') as f:
                f.write(e.response.content)
