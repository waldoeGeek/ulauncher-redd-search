import os
from urllib.parse import urlparse
import urllib.request as req
import requests

def save_thumbnail(thumb_url):
    # get thumbnail
    file = urlparse(thumb_url)
    # get thumbnail filename
    file_path = os.path.basename(file.path)
    icon_path = 'images/thumbs/' + file_path
    url = thumb_url
    req.urlretrieve(url, icon_path)
