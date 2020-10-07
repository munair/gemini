#!/usr/bin/env python3


# Strategy Outline:
#  1. Want to purchase DAI at a specific price.
#  2. The bid size is limited by a USD (quote currency) budget.
#
# Execution:
#   - Copy this file from the strategies directory to the level below. Run with python3.

import json
import requests

from decimal import Decimal

from libraries.logger import logger
from libraries.dealseaker import pricedrop
from libraries.liquiditymaker import quotabid
from libraries.fillvalidator import confirmexecution


# Set quote currency (USD in this case) budget.
# This amount should exceed 20 cents ['0.1' is the minimum for DAIUSD].
# Configure price drop desired in decimal terms.
# For example, 20 basis points is '0.002'. This covers Gemini API trading fees round trip!
pair = 'DAIUSD'
cash = '0.25'
cost = '1.00760'

# Submit limit bid order.
logger.debug(f'submitting {pair} limit bid order: {cost} bid on a {cost} budget.')
post = quotabid( pair, cash, cost )
post = post.json()
dump = json.dumps( post, sort_keys=True, indent=4, separators=(',', ': ') )
logger.debug ( dump )

# Define poststatus class.
# Purpose: Stores the state of the orderid parameter upon exiting the websocket connection session.
class Poststatus:
    def __init__(self, state): self.__state = state
    def getvalue(self): return self.__state
    def setvalue(self, state): self.__state = state

poststatus = Poststatus(False)

# Determine if the order was filled.
confirmexecution( orderid = post['order_id'], poststatus = poststatus )
