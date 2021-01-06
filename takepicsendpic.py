#!/usr/bin/env python

import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def takepic(name, path="."):
    os.system('fswebcam %s/%s.jpg', path, name)

def sendpic(name, path):
    mp_encoder = MultipartEncoder(
        fields={
            'id': '249824748730293804',
            # plain file object, no filename or mime type produces a
            # Content-Disposition header with just the part name
            'picture': ('pic1.jpg', open('bruh.jpg', 'rb'), 'image/x-icon'),
        }
    )
    r = requests.post(
        'https://iotgreenhousedata.azurewebsites.net/api/UploadPicture',
        data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
        # The MultipartEncoder provides the content-type header with the boundary:
        headers={'Content-Type': mp_encoder.content_type}
    )