from src.video import Video


class Channel:

    def __init__(self, name, video_count, view_count, upload_playlist_id, channel_id, subscriber_count=-1):
        self.name = name
        self.video_count = video_count
        self.view_count = view_count
        self.channel_id = channel_id
        self.subscriber_count = subscriber_count
        self.upload_playlist_id = upload_playlist_id
        self.videos = []

    def set_videos(self, videos):
        self.videos = videos

    def get_average_views_per_video(self):
        total_views = 0
        for video in self.videos:
            total_views += int(video.view_count)
        return round(total_views / len(self.videos)).__format__(",").replace(",", " ")

    def get_average_likes_per_video(self):
        total_likes = 0
        for video in self.videos:
            total_likes += int(video.like_count)
        return round(total_likes / len(self.videos)).__format__(",").replace(",", " ")

    def to_json(self):
        return {
            "name": self.name,
            "video_count": self.video_count,
            "view_count": self.view_count,
            "channel_id": self.channel_id,
            "subscriber_count": self.subscriber_count,
            "upload_playlist_id": self.upload_playlist_id,
            "videos": [video.to_json() for video in self.videos]
        }

    @classmethod
    def from_json(cls, channel_json):
        channel = cls(channel_json["name"], channel_json["video_count"], channel_json["view_count"],
                      channel_json["upload_playlist_id"], channel_json["channel_id"], channel_json["subscriber_count"])
        channel.set_videos([Video.from_json(video_json) for video_json in channel_json["videos"]])
        return channel

    def __str__(self):
        return f"""Channel: {self.name}
Chnnel ID: {self.channel_id}
Total videos: {int(self.video_count).__format__(",").replace(",", " ")}
Total views: {int(self.view_count).__format__(",").replace(",", " ")}
Total subscribers: {int(self.subscriber_count).__format__(",").replace(",", " ")}"""
