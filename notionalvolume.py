#!/usr/bin/env python3


# Strategy Outline:
#  1. Retrieve the 30-day (USD-denominated) notional volume and trading fees.
#
# Execution:
#   - Use the wrapper BASH script in the "strategies" directory.

import sys
import json
import requests
import locale

from libraries.logger import logger
from libraries.volumizer import notionalvolume


# Set default field value.
field = ''

# Override defaults with command line parameters.
if len(sys.argv) == 2:
    field = sys.argv[1]

# Submit request.
logger.debug(f'submitting request...')
post = notionalvolume()
data = post.json()
dump = json.dumps( data, sort_keys=True, indent=4, separators=(',', ': ') )


# Format response.
if field == 'notional_30d_volume': print( f'your notional 30-day volume is {post.json()["notional_30d_volume"]:,.2} USD.' )


# Let the shell know we successfully made it this far!
if post: sys.exit(0)
else: sys.exit(1)