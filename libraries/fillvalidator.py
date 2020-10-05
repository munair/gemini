#!/usr/bin/env python3


import requests
import ssl
import json
import websocket
import datetime
import time

from decimal import Decimal

from libraries.logger import logger as logger
from libraries.messenger import smsalert as smsalert

import libraries.authenticator as authenticator
import libraries.resourcelocator as resourcelocator

def confirmexecution(
        orderid: str,
        poststatus: object
    ) -> None:

    # Introduce function.
    logger.debug(f'Confirming execution of the order identified by the Gemini assigned number: {orderid}')

    # Define websocet functions.
    def on_close(ws): logger.debug(f'{ws} connection closed.')
    def on_open(ws): logger.debug(f'{ws} connection opened.')
    def on_error(ws, error): logger.debug(error)
    def on_message(ws, message, orderid=orderid):
        dictionary = json.loads( message )
        # Remove comment to debug with: logger.info( dictionary )

        if isinstance(dictionary, list):
            for listitem in dictionary:
                exitstatus = False
                if listitem['order_id'] == orderid:
                    # Exit upon receiving order cancellation message.
                    if listitem['is_cancelled']: exitstatus = f'Order {orderid} was cancelled.'
                    if listitem['type'] == 'cancelled': exitstatus = f'Order {orderid} was cancelled [reason:{listitem["reason"]}].'
                    if listitem['type'] == 'rejected': exitstatus = f'Order {orderid} was rejected.'
                    if listitem['type'] == 'fill':
                        # Make sure that the order was completely filled.
                        if listitem['remaining_amount'] == '0': exitstatus = f'Order {orderid} was filled.'
                if exitstatus:
                    ws.close()
                    logger.debug( exitstatus )
                    smsalert ( exitstatus )
                    poststatus.setvalue( True )

    # Construct payload.
    endpoint = '/v1/order/events'
    nonce = int(time.time()*1000)
    payload = {
        'request': endpoint,
        'nonce': nonce
    }
    header = authenticator.authenticate(payload)

    # Establish websocket connection.
    ws = websocket.WebSocketApp(str( resourcelocator.sockserver + endpoint ),
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                header = header['sockheader'])
    ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
