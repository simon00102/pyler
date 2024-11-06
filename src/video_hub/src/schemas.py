from pydantic import BaseModel
from datetime import datetime


class VideoCreate(BaseModel):
    video_url : str

class VideoResponse(BaseModel):
    video_id: str
    title: str | None = None
    description: str | None = None
    upload_time: datetime | None = None
    thumbnail: str | None = None
    channel_id: str | None = None
    category_id: int | None = None
    duration: int | None = None

class VideoStatisticsSeriesResponse(BaseModel):
    video_id: str
    crawl_time: datetime
    views: int
    likes: int
    comments: int

class VideoStatisticsChange(BaseModel):
    views_change: int
    likes_change: int
    comments_change: int

class VideoStatisticsResponse(BaseModel):
    video_id: str
    from_datetime: datetime
    to_datetime: datetime
    changes: VideoStatisticsChange
    start_time: datetime
    end_time: datetime

class TotalVideoStatisticsResponse(BaseModel):
    from_datetime: datetime
    to_datetime: datetime
    changes: VideoStatisticsChange