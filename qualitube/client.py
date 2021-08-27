"""
MIT License

Copyright (c) 2021 Vítor Mussa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import List, Dict, Any

import requests

from .video import Video, VideosResponse
from .exceptions import QualitubeException


__all__ = ('Client',)


class Client:
    """Represents the customer with the Google API."""

    BASE_URL = 'https://youtube.googleapis.com/youtube/v3'

    __slots__ = ('api_key')

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def get_videos(self, videos: List[str]) -> VideosResponse:
        """Returns a dataset with analytics data of the given video
        IDs.
        """
        endpoint = f'{Client.BASE_URL}/videos'
        ret: List[Video] = []

        headers = {'Accept': 'application/json'}

        params: Dict[str, str] = {}
        params['part'] = 'snippet,statistics'
        params['key'] = self.api_key

        while videos:
            params['id'] = ','.join(videos[-50:])
            del videos[-50:]
            
            res = requests.get(endpoint, headers=headers, params=params)
            json: Dict[str, Any] = res.json()

            if (error := json.get('error')):
                raise QualitubeException(error['message'])

            for item in json['items']:
                ret.append(Video(item))

        return VideosResponse(videos=ret)
