import os
from urllib.parse import urlparse
import urllib.request as req
import requests

base_url = 'https://reddit.com/search.json?q='


class Searches:


    def save_thumbnail(thumb_url):
        # get thumbnail
        file = urlparse(thumb_url)
        # get thumbnail filename
        file_path = os.path.basename(file.path)
        icon_path = 'images/thumbs/' + file_path
        url = thumb_url
        req.urlretrieve(url, icon_path)


    def result_type_url(url, query, type):
        url = url
        url = url + query + '&type=' + type
        return url


    def get_results(url, query):
        type = 'all'
        query = query
        url = 'https://www.reddit.com/search.json?q=' + query

        response = requests.get(url, headers = {'User-Agent': 'google'})

        data = response.json()
        data = data['data']['children']

        #Check for empty results
        if not data:
            return 'No Results!'
        else:
            for child in data:
                child['data']['subreddit'] = f"/r/{child['data']['subreddit']}"

            return data



    def get_users(url, query):
        type = 'user'
        query = query
        # url = 'https://reddit.com/search.json?q=knives&type=user'
        url = Searches.result_type_url(url, query, type)
        # url = url + query + '&type=' + type

        response = requests.get(url, headers = {'User-Agent': 'google'})

        data = response.json()
        data = data['data']['children']

        # Check for empty results
        if not data:
            return 'No Results!'
        else:
            for child in data:
                user_url = f"{child['data']['subreddit']['url']}"
                child['data']['permalink'] = user_url
                child['data']['subreddit'] = f"/{child['data']['subreddit']['display_name_prefixed']}"
                child['data']['title'] = child['data']['name']


            return data


    def get_subs(url, query):

        type = 'sr'
        query = query
        url = Searches.result_type_url(url, query, type)

        response = requests.get(url, headers = {'User-Agent': 'google'})

        data = response.json()
        data = data['data']['children']

        # Check for empty results
        if not data:
            return 'No Results'
        else:
            for child in data:
                sub_reddit_value = child['data']['public_description']
                child['data']['subreddit'] = sub_reddit_value
                child['data']['title'] = child['data']['display_name_prefixed']
                child['data']['permalink'] = f"/{child['data']['title']}"

            return data
