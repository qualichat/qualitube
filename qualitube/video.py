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

from typing import Dict, Any, Optional, List

from pandas import DataFrame


__all__ = ('Video',)


def _try_parse_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None

    return int(value)


class Video:
    """Represents a dataset from a video returned by the Google API."""

    __slots__ = (
        'id', 'title', 'description', 'tags', 'view_count', 'like_count',
        'dislike_count', 'favorite_count', 'comment_count'
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.id: Optional[str] = payload.get('id', None)

        snippets = payload.get('snippet', {})
        self.title: Optional[str] = snippets.get('title', None)
        self.description: Optional[str] = snippets.get('description', None)
        self.tags: Optional[List[str]] = snippets.get('tags', None)

        # Statistics
        statistics = payload.get('statistics', {})

        view_count = _try_parse_int(statistics.get('viewCount'))
        self.view_count: Optional[int] = view_count

        like_count = _try_parse_int(statistics.get('likeCount'))
        self.like_count = like_count

        dislike_count = _try_parse_int(statistics.get('dislikeCount'))
        self.dislike_count = dislike_count

        favorite_count = _try_parse_int(statistics.get('favoriteCount'))
        self.favorite_count = favorite_count

        comment_count = _try_parse_int(statistics.get('commentCount'))
        self.comment_count = comment_count

    def __repr__(self) -> str:
        return f'<Video id={self.id!r}>'


class VideosResponse:
    """Represents a response from a Google API video dataset."""

    __slots__ = ('videos')

    def __init__(self, videos: List[Video]) -> None:
        self.videos: List[Video] = videos

    def __repr__(self) -> str:
        return f'<VideosResponse videos={self.videos}>'

    def to_dataframe(self) -> DataFrame:
        """Transforms the video dataset into a dataframe."""
        rows: List[List[Any]] = []
        columns = Video.__slots__

        for video in self.videos:
            rows.append([
                video.id, video.title, video.description, video.tags, video.view_count,
                video.like_count, video.dislike_count, video.favorite_count,
                video.comment_count
            ])
        
        return DataFrame(rows, columns=columns) # type: ignore
