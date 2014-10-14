#!/usr/bin/env python
# coding: utf-8
"""
This is an example of using pymco to replicate 'mco puppet status'
Be advised this is currently fragile and will break. I'm not reading the DDL
or anything like I should. I simply watched what `mco puppet status` sends
over the wire in its message body, and replicated it.

Note that pymco itself should probably attempt to serialize the message body
if it's a dict, and should deserialize the reply body if it appears to be
YAML. Right now, we're handling that here.
"""
import logging

from pymco import config
from pymco import rpc
from pymco import message
import time
import pprint

# logging
FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(name)s.%(funcName)s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

# read the config as a Config object
logger.debug("reading config...")
config = config.Config.from_configfile('client.cfg')

# construct a dict/hash to send as the message body
msg_data = {':action': 'status', ':data': {':process_results': True}, ':ssl_ttl': 60, ':ssl_msgtime': int(time.time())}
logger.debug("msg_data:\n{m}".format(m=msg_data))

# serialize the message body
serializer = config.get_serializer('plugin.ssl_serializer')
msg_body = serializer.serialize(msg_data)
logger.debug("msg_body: \n{m}".format(m=msg_body))

# construct the Message itself
msg = message.Message(body=msg_body, agent='puppet', config=config)
logger.debug("calling rpc.SimpleAction")
action = rpc.SimpleAction(config=config, msg=msg, agent='puppet')
logger.debug("SimpleAction.call()")
results = action.call()
# loop through the results, and deserialize their bodies
for r in results:
    r['body'] = serializer.deserialize(r['body'])
    pprint.pprint(r)
