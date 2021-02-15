#!/usr/bin/python3
import json
import requests

reddit_url = 'https://reddit.com/search.json?q='
search_term = 'knives'
full_url = reddit_url + search_term
response = requests.get(full_url, headers = {'User-agent': 'google'})
data = response.json()
data = data['data']['children'] #get the children data from response
# i = 0
# #loop through the children print title, thumbnail url and url of each
# while i <= len(data) - 1:
#     title = data[i]['data']['title']
#     thumbnail = data[i]['data']['thumbnail']
#     url = data[i]['data']['permalink']
#     print(title)
#     print(thumbnail)
#     print(f'URL: https://www.reddit.com/{thumbnail}')
#     i = i + 1

for child in data:
    title = child['data']['title']
    thumb = child['data']['thumbnail']
    child_url = child['data']['permalink']
    print(title)
    print(thumb)
    print(f'URL: https://www.reddit.com/{child_url}')
