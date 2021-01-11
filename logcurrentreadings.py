#!/usr/bin/env python

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def toLogs(data):
    f = open("logfile", "a")
    f.write(data)
    f.close

def sendLog(data, id = '249824748730293804'):
    print(f'sending log data {data}')
    mp_encoder = MultipartEncoder(
        fields={
            'id': id,
            # plain file object, no filename or mime type produces a
            # Content-Disposition header with just the part name
            'temperature': data[0],
            'brightness1': data[1],
            'brightness2': data[2],
            'brightness3': data[3],
            'brightness4': data[4],
            'moistureair': data[5],
            'moistureground': data[6],
            'score': 69
        }
    )
    r = requests.post(
        'https://iotgreenhousedata.azurewebsites.net/api/UploadLogs',
        data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
        # The MultipartEncoder provides the content-type header with the boundary:
        headers={'Content-Type': mp_encoder.content_type}
    )