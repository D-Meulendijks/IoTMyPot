#!/usr/bin/env python

import hardwarespi
import takepicsendpic
import logcurrentreadings
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os


def take_image_and_send():
    now = datetime.now()
    t = now.strftime("%H_%M_%S")
    namecurrtimepic = "image" + t + '.jpg'       # get current time to save with timestamp
    takepicsendpic.takePic(namecurrtimepic, "./pics")   # take the picture and save it
    takepicsendpic.sendPic(namecurrtimepic, "./pics")   # take the saved picture and send it to the database

def take_measurements_and_send():
    namecurrtimemeasure = datetime.datetime.now()       # get current time to save with timestamp
    data = [hardwarespi.read_spi(i) for i in range(8)]  # read pin on MCP3008
    logcurrentreadings.tologs(data)                     # save the readings to a log file
    logcurrentreadings.sendLog(data)                    # send all the readings to the database



if __name__ == '__main__':
    print("Setup hardware spi")
    hardwarespi.setup_spi()
    os.system("chromium-browser --start-fullscreen www.google.com")
    print("Browser opened")

    # Calls the function take_image_and_send every hour
    print("Start pic scheduler")
    picscheduler = BlockingScheduler()
    picscheduler.add_job(take_image_and_send, 'interval', seconds=5)
    picscheduler.start()
    # Calls the function take_measurements_and_send every 30 minutes
    print("Start meas scheduler")
    measscheduler = BlockingScheduler()
    measscheduler.add_job(take_measurements_and_send, 'interval', seconds=5)
    measscheduler.start()
    print("Setup done")
    # Open web browser and go to interface site