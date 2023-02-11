class Video:
    def __init__(self, title, url, date, time):
        self.title = title
        self.url = url
        self.date = date
        self.time = time
        self.view_count = 0
        self.like_count = 0
        self.comment_count = 0
        self.duration = ""
        self.is_short = False

    def set(self, view_count, like_count, comment_count, duration):
        self.view_count = int(view_count)
        self.like_count = int(like_count)
        self.comment_count = int(comment_count)
        self.duration = duration
        self.is_short = self.get_duration() < 60

    def to_json(self):
        return {
            "title": self.title,
            "url": self.url,
            "date": self.date,
            "time": self.time,
            "view_count": str(self.view_count),
            "like_count": str(self.like_count),
            "comment_count": str(self.comment_count),
            "duration": str(self.duration),
            "is_short": self.is_short,
        }

    @staticmethod
    def from_json(json):
        video = Video(json["title"], json["url"], json["date"], json["time"], )
        video.view_count = int(json["view_count"])
        video.like_count = int(json["like_count"])
        video.comment_count = int(json["comment_count"])
        video.duration = json["duration"]
        video.is_short = json["is_short"]
        return video

    def get_duration(self):
        dur_str = self.duration
        dur_str = dur_str.replace("PT", "")
        hours = 0
        minutes = 0
        seconds = 0
        if "H" in dur_str:
            hours = int(dur_str.split("H")[0])
            dur_str = dur_str.split("H")[1]
        if "M" in dur_str:
            minutes = int(dur_str.split("M")[0])
            dur_str = dur_str.split("M")[1]
        if "S" in dur_str:
            seconds = int(dur_str.split("S")[0])
        return hours * 3600 + minutes * 60 + seconds
