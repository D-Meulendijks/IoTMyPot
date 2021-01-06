#!/usr/bin/env python

import hardwarespi
import takepicsendpic
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import logcurrentreadings


def take_image_and_send():
    namecurrtime = datetime.datetime.now()
    takepicsendpic.takepic(namecurrtime, "./pics")
    takepicsendpic.sendpic(namecurrtime, "./pics")



if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(take_image_and_send, 'interval', hours=1)
    scheduler.start()
    hardwarespi.setup_spi()
    while True:
        try:
            data = [hardwarespi.read_spi(i) for i in range(8)] #maybe if this is wrong set it to range(1,9) # read pin on MCP3008
            logcurrentreadings.tologs(data)
        finally:
            pass
