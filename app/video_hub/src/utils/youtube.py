import re
from typing import Optional
from datetime import datetime, timezone
import requests
from models import Video, VideoStatistics
from configure import YOUTUBE_API_KEY


def parse_duration(duration_str : str) -> int:
    '''ISO 8601 포맷의 동영상 길이를 초 단위로 변환'''
    hours, minutes, seconds = 0, 0, 0
    duration_str = duration_str.replace("PT", "")
    if "H" in duration_str:
        hours = int(duration_str.split("H")[0])
        duration_str = duration_str.split("H")[1]
    if "M" in duration_str:
        minutes = int(duration_str.split("M")[0])
        duration_str = duration_str.split("M")[1]
    if "S" in duration_str:
        seconds = int(duration_str.split("S")[0])
    return hours * 3600 + minutes * 60 + seconds

def fetch_video_data(video_id: str):
    '''YouTube API를 통해 video_id에 해당하는 비디오 정보를 가져와 Video와 VideoStatistics 객체를 생성'''
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': video_id,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        video_data = response.json().get('items', [None])[0]
        if not video_data:
            print("No video data found.")
            return None, None
        
        snippet = video_data.get("snippet", {})
        content_details = video_data.get("contentDetails", {})
        statistics = video_data.get("statistics", {})
        
        video = Video(
            video_id=video_data["id"],
            title=snippet.get("title"),
            description=snippet.get("description"),
            upload_time=datetime.fromisoformat(snippet.get("publishedAt").replace("Z", "+00:00")),
            thumbnail=snippet.get("thumbnails", {}).get("high", {}).get("url"),
            channel_id=snippet.get("channelId"),
            category_id=int(snippet.get("categoryId", 0)) if snippet.get("categoryId") else None,
            duration=parse_duration(content_details.get("duration", "PT0S"))
        )
        
        video_statistics = VideoStatistics(
            video_id=video_data["id"],
            crawl_time=datetime.now(timezone.utc),
            views=int(statistics.get("viewCount", 0)),
            likes=int(statistics.get("likeCount", 0)),
            comments=int(statistics.get("commentCount", 0))
        )
        
        return video, video_statistics
    else:
        print(f"Error: {response.status_code}")
        return None, None
    
def extract_video_id(url: str) -> Optional[str]:
    '''youtube url 주소에서 video_id를 추출'''
    long_url_pattern = r"^https?://(www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})"
    short_url_pattern = r"^https?://youtu\.be/([a-zA-Z0-9_-]{11})"

    long_url_match = re.match(long_url_pattern, url)
    if long_url_match:
        return long_url_match.group(2)  # video_id 반환

    short_url_match = re.match(short_url_pattern, url)
    if short_url_match:
        return short_url_match.group(1)  # video_id 반환

    return None
