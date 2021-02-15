## Reddit Search Extension
#By: waldoeGeek

import os
import json
import requests
from urllib.parse import urlparse

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from src.functions import save_thumbnail

REDDIT_URL = 'https://reddit.com/search.json?q='
ICON_FILE = 'images/icon.png'


class RedditExtension(Extension):

    def __init__(self):
        super(RedditExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        try:
            items = []
            query = event.get_argument() or ""

            if len(query) < 3:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon=ICON_FILE,
                        name='Keep Typing to Search on Reddit....',
                        on_enter=HideWindowAction(),
                        highlightable=False
                    )
                ])

            ######
            # Check for result type
            #
            # if extension.preferences['result_types'] == 'all':
            #     type = ''
            #     # full_url = REDDIT_URL + query
            # elif extension.preferences['result_types'] == 'subs':
            #     type = '&type=sr'
            #     # full_url = REDDIT_URL + query + '&type=sr'
            # elif extension.preferences['result_types'] == 'users':
            #     type = '&type=user'
            #     # full_url = REDDIT_URL + query + '&type=user'

            full_url = REDDIT_URL + query
            response = requests.get(full_url, headers = {'User-Agent': 'google'})
            data = response.json()
            data = data['data']['children']
            max_results = int(extension.preferences['max_results'])
            for child in data[0:max_results]:
                permalink = child['data']['permalink']
                child_url = f"https://reddit.com{permalink}"
                ico_url = child['data']['thumbnail']

                if extension.preferences['show_thumbnails'] == 'true':
                    try:
                        save_thumbnail(child['data']['thumbnail'])
                        file = urlparse(os.path.basename(ico_url.path))
                        ico_path = f'images/thumbs/{file}'
                    except Exception as e:
                        ico_path = f'images/icon.png'
                else:
                    ico_path = 'images/icon.png'

                items.append(ExtensionResultItem(
                    icon=ico_path or ICON_FILE,
                    # icon=icon_path,
                    # icon=child['data']['thumbnail'] or ICON_FILE,
                    name=child['data']['title'],
                    description=f"/r/{child['data']['subreddit']}",
                    on_enter=OpenUrlAction(child_url)
                ))

            return RenderResultListAction(items)

        except Exception as e:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='ERROR',
                                             description='No items Found!',
                                             on_enter=HideWindowAction()))

            return RenderResultListAction(items)

if __name__ == '__main__':
    RedditExtension().run()
