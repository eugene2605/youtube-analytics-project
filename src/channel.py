import json
import os
from googleapiclient.discovery import build
# import isodate

api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name):
        """Сохраняет в файл 'moscowpython.json' значения атрибутов экземпляра Channel"""
        attributes = {'channel_id': self.__channel_id,
                      'title': self.title,
                      'description': self.description,
                      'url': self.url,
                      'subscriber_count': self.subscriber_count,
                      'video_count': self.video_count,
                      'view_count': self.view_count}
        with open(os.path.join("..", "src", file_name), 'w', encoding='utf-8') as file:
            json.dump(attributes, file, indent=2, ensure_ascii=False)
