#!/usr/bin/env python
# coding: utf-8
import logging
import pprint

from pymco import config
from pymco import rpc
from pymco import message

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(name)s.%(funcName)s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

config = config.Config.from_configfile('client.cfg')
msg = message.Message(body='ping', agent='discovery', config=config)
logger.debug("calling rpc.SimpleAction")
action = rpc.SimpleAction(config=config, msg=msg, agent='discovery')
logger.debug("SimpleAction call finished")
results = action.call()
pprint.pprint(results)
