#! /bin/bash
#
# script name: premiumbtcusdask.bash
# script author: munair simpson
# script created: 20210303
# script purpose: (base currency) ask for USD (providing BTC)

# SHORT on BTC and LONG on USD, where:
# Parameter 0 is the pair.
# Parameter 1 is the order size in terms of the base currency (0.07765 is 0.07765 BTC).
# Parameter 2 is the premium (0.03 is a 3% premium).
python3 ../premiumfrontrunningask.py BTCUSD 0.32468703 0.076 && echo success!

# Warning: Does not manage bid/ask irregularities well. It is suggested that you use quotask based scripts.
