#!/usr/bin/env python

import hardwarespi
import takepicsendpic
import logcurrentreadings
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def take_image_and_send():
    namecurrtimepic = datetime.datetime.now()           # get current time to save with timestamp
    takepicsendpic.takepic(namecurrtimepic, "./pics")   # take the picture and save it
    takepicsendpic.sendpic(namecurrtimepic, "./pics")   # take the saved picture and send it to the database

def take_measurements_and_send():
    namecurrtimemeasure = datetime.datetime.now()       # get current time to save with timestamp
    data = [hardwarespi.read_spi(i) for i in range(8)]  # read pin on MCP3008
    logcurrentreadings.tologs(data)                     # save the readings to a log file



if __name__ == '__main__':
    hardwarespi.setup_spi()

    # Calls the function take_image_and_send every hour
    picscheduler = BlockingScheduler()
    picscheduler.add_job(take_image_and_send, 'interval', hours=1)
    picscheduler.start()
    # Calls the function take_measurements_and_send every 30 minutes
    measscheduler = BlockingScheduler()
    measscheduler.add_job(take_measurements_and_send, 'interval', minutes=30)
    measscheduler.start()