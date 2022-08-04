#! /bin/bash
#
# script name: discountyfiusdquotaask.bash
# script author: munair simpson
# script created: 20201031
# script purpose: ask on YFI using USD on quota

# LONG on YFI and SHORT on USD, where:
# LONG on YFI and SHORT on USD, where:
# Parameter 0 is the pair.
# Parameter 1 is the budget (100 is 100 USD).
# Parameter 2 is the discount (0.02 is a 2% discount).
python3 ../discountquotafrontrunning.py YFIUSD 500 0.01 && echo success!
