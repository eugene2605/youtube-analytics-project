import os
from googleapiclient.discovery import build

api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для ютуб-видео"""

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video = youtube.videos().list(id=self.video_id,
                                           part='snippet,statistics,contentDetails,topicDetails'
                                           ).execute()
        self.title = self.video['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch/' + self.video_id
        self.view_count = int(self.video['items'][0]['statistics']['viewCount'])
        self.like_count = int(self.video['items'][0]['statistics']['likeCount'])

    def __str__(self):
        """Возвращает название ютуб-видео"""
        return self.title


class PLVideo(Video):
    """Класс для ютуб-плейлиста"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        """Возвращает название ютуб-видео"""
        return self.title
