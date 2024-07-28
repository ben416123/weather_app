import sys
import argparse
import os

from weatherapp.core import parser_loader
from weatherapp.core import ForecastType
from weatherapp.core.unit import Unit
from weatherapp.core import SetUnitAction


def _validate_forecast_args(args):
    if args.forecast_option is None:
        error_msg = ('One of these arguments must be used:'
                     '-td/--today, -5d/--fivedays, -10d/--tendays, -w/--weekend')
        print(f'error: {error_msg}',
              file=sys.stderr)
        sys.exit()


current_dir = os.path.dirname(os.path.abspath(__file__))
parsers_dir = os.path.join(current_dir, '../parsers')

parsers = parser_loader.load(parsers_dir)
argparser = argparse.ArgumentParser(
    prog='weatherapp',
    description='Weather info from weather.com on your terminal')

required = argparser.add_argument_group('required arguments')

required.add_argument('-p', '--parser',
                      choices=parsers.keys(),
                      required=True,
                      dest='parser',
                      help='Specify which parser is going to be used to scrape weather information.')

unit_values = [name.title() for name, value in
               Unit.__members__.items()]

argparser.add_argument('-u', '--unit',
                       choices=unit_values,
                       required=False,
                       action=SetUnitAction,
                       dest='unit',
                       help='Specify the unit that will be used to display the temperatures')

required.add_argument('-a', '--areacode',
                      required=True,
                      dest='area_code',
                      help='The code area to get the weather broadcast from. They can be retrieved from weather.com')

argparser.add_argument('-v', '--version',
                       action='version',
                       version='%(prog)s 1.0')

argparser.add_argument('-td', '--today',
                       dest='forecast_option',
                       action='store_const',
                       const=ForecastType.TODAY,
                       help='Show the weather forecast for the current day')

args = argparser.parse_args()

_validate_forecast_args(args)

cls = parsers[args.parser]

parser = cls()

results = parser.run(args)

for result in results:
    print(results)
