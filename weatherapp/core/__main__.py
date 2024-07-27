import sys
import argparse

from weatherapp.core import parser_loader
from weatherapp.core import ForecastType
from weatherapp.core.unit import Unit


def _validate_forecast_args(args):
    if args.forecast_option is None:
        error_msg = ('One of these arguments must be used:'
                     '-td/--today, -5d/--fivedays, -10d/--tendays, -w/--weekend')
        print(f'error: {error_msg}',
              file=sys.stderr)
        sys.exit()


parsers = parser_loader.load('./weatherterm/parsers')
argparser = argparse.ArgumentParser(
    prog='weatherterm',
    description='Weather info from weather.com on your terminal')

required = argparser.add_argument_group('required arguments')

required.add_argument('-p', '--parser',
                      choices=parsers.keys(),
                      required=True,
                      dest='parser',
                      help='Specify which parser is going to be used to scrape weather information.')

unit_values = [name.title() for name, value in
               Unit.__members__.items()]
