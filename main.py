#!/usr/bin/env python

import hardwarespi
import takepicsendpic
import logcurrentreadings
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os


def take_image_and_send():
    now = datetime.now()
    t = now.strftime("_%d_%m_%y_%H_%M_%S")
    namecurrtimepic = "image" + t + '.jpg'       # get current time to save with timestamp
    takepicsendpic.takePic(namecurrtimepic, "./pics")   # take the picture and save it
    takepicsendpic.sendPic(namecurrtimepic, "./pics")   # take the saved picture and send it to the database


def take_measurements_and_send():
    # now = datetime.now()
    # t = now.strftime("%H_%M_%S")
    # namecurrtimemeasure = t       # get current time to save with timestamp
    data = [hardwarespi.read_spi(i) for i in range(8)]  # read pin on MCP3008
    print(f"@@@@@ - > data measured {data}")
#    logcurrentreadings.toLogs(data)                     # save the readings to a log file
    logcurrentreadings.sendLog(data)                    # send all the readings to the database


def docycle():
    take_image_and_send()
    take_measurements_and_send()


if __name__ == '__main__':
    UUID = '249824748730293804'
    print("Setup hardware spi")
    hardwarespi.setup_spi()
    os.system(f"chromium-browser --start-fullscreen https://victorious-mushroom-07a4faf03.azurestaticapps.net?key={UUID}")
    print("Browser opened")

    # Calls the function take_image_and_send every hour
    print("Start pic scheduler")
    picscheduler = BlockingScheduler()
    picscheduler.add_job(docycle, 'interval', seconds=20)
    picscheduler.start()
    # Calls the function take_measurements_and_send every 30 minutes
    print("Setup done")
    # Open web browser and go to interface site