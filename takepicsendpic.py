#!/usr/bin/env python

import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def takePic(name, path="."):
    print(f'taking picture and saving to {path}/{name}')
    os.system(f'fswebcam {path}/{name}')
    print('saved')


def sendPic(name, path = '.', id = '249824748730293804'):
    print(f'sending picture from {path}/{name}')
    filepath = path + '/' + name
    mp_encoder = MultipartEncoder(
        fields={
            'id': id,
            # plain file object, no filename or mime type produces a
            # Content-Disposition header with just the part name
            'picture': (name, open(filepath, 'rb'), 'image/x-icon'),
        }
    )
    r = requests.post(
        'https://iotgreenhousedata.azurewebsites.net/api/UploadPicture',
        data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
        # The MultipartEncoder provides the content-type header with the boundary:
        headers={'Content-Type': mp_encoder.content_type}
    )