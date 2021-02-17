## Reddit Search Extension
#By: waldoeGeek

import os
import json
import requests

from urllib.parse import urlparse
from src.functions import Searches
# from src.functions import save_thumbnail
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction


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
                        on_enter=DoNothingAction(),
                        highlightable=False
                    )
                ])

        # Check result type options
            try:
                # if extension.preferences["result_types"] == 'all':
                #     data = Searches.get_results(REDDIT_URL, query)
                # elif extension.preferences['result_types'] == 'sub':
                #     data = Searches.get_subs(REDDIT_URL, query)
                # elif extension.preferences['result_types'] == 'user':
                #     data = Searches.get_users(REDDIT_URL, query)
                keyword = event.get_keyword()
                for kw_id, kw in list(extension.preferences.items()):
                    if kw == keyword:
                        keyword_id = kw_id

                data = Searches.get_results(REDDIT_URL, query)
                if keyword_id == "rtu_kw":
                    data = Searches.get_users(REDDIT_URL, query)
                elif keyword_id == "rtr_kw":
                    data = Searches.get_subs(REDDIT_URL, query)

            except Exception as e:
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'ERROR {e}',
                    description='failed at keyword',
                    on_enter=HideWindowAction()))

                return RenderResultListAction(items)


            max_results = int(extension.preferences['max_results'])
            for child in data[0:max_results]:
                permalink = child['data']['permalink']
                child_url = f"https://www.reddit.com{permalink}"

                items.append(ExtensionResultItem(
                    icon=ICON_FILE,
                    name=child['data']['title'],
                    description=f"{child['data']['subreddit']}",
                    on_enter=OpenUrlAction(child_url)
                ))

            return RenderResultListAction(items)
        except Exception as e:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='ERROR',
                description='No items Found!',
                on_enter=HideWindowAction()))

            return RenderResultListAction(items)


if __name__ == '__main__':
    RedditExtension().run()
