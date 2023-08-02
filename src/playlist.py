import os
from datetime import timedelta
import isodate as isodate
from googleapiclient.discovery import build

api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """Класс для ютуб-плейлиста"""

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста."""
        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(id='PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw',
                                                 part='contentDetails,snippet',
                                                 maxResults=50,
                                                 ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id

    def youtube_requests(self):
        """Возвращает данные по видеороликам в плейлисте"""
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        return video_response

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        video_response = self.youtube_requests()
        total_duration = timedelta(0)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        video_response = self.youtube_requests()
        like_count = 0
        best_video_id = ''
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > like_count:
                best_video_id = video['id']
                like_count = int(video['statistics']['likeCount'])
        best_video_url = 'https://youtu.be/' + best_video_id
        return best_video_url
