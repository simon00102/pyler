import asyncio
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Video
from cores.videos import fetch_video_data


async def generate_statistics():
    '''1시간 주기로 Youtube 통계 정보를 새로 삽입하는 task'''
    while True:
        db: Session = SessionLocal()
        
        try:
            await insert_video_statistics(db)
        finally:
            db.close()
        
        await asyncio.sleep(3600)


async def insert_video_statistics(db: Session):
    '''모든 비디오에 대한 최신 통계 정보를 삽입'''
    current_time: datetime = datetime.now(timezone.utc)
    videos = db.query(Video).all()
    
    for video in videos:
        _, video_statistics = fetch_video_data(video.video_id)

        if video_statistics is None:
            continue

        video_statistics.crawl_time = current_time
        db.add(video_statistics)

    db.commit()
