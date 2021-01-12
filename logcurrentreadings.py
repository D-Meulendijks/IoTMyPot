#!/usr/bin/env python

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def toLogs(data):
    f = open("logfile", "a")
    f.write(data)
    f.close

def sendLog(data_received, id = '249824748730293804'):
    print(f'sending log data {data_received}')
    data_received_int = [str(i) for i in data_received]
    mp_encoder = MultipartEncoder(
        fields={
            'id': id,
            # plain file object, no filename or mime type produces a
            # Content-Disposition header with just the part name
            'temperature': data_received_int[0],
            'brightness1': data_received_int[1],
            'brightness2': data_received_int[2],
            'brightness3': data_received_int[3],
            'brightness4': data_received_int[4],
            'moistureair': data_received_int[5],
            'moistureground': data_received_int[6],
            'score': data_received_int[7]
        }
    )
    r = requests.post(
        'https://iotgreenhousedata.azurewebsites.net/api/UploadLogs',
        data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
        # The MultipartEncoder provides the content-type header with the boundary:
        headers={'Content-Type': mp_encoder.content_type}
    )