from datetime import datetime
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Video(Base):
    '''비디오 메타 데이터 정보'''
    __tablename__ = "video_metadata"

    video_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)  # YouTube VIDEO_ID
    title: Mapped[str] = mapped_column(String, nullable=True)  # Title
    description: Mapped[str] = mapped_column(String, nullable=True)  # Description
    upload_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Upload Time
    thumbnail: Mapped[str] = mapped_column(String, nullable=True)  # Thumbnail URL
    channel_id: Mapped[str] = mapped_column(String, nullable=True)  # Channel ID
    category_id: Mapped[int] = mapped_column(Integer, nullable=True)  # Category ID
    duration: Mapped[int] = mapped_column(Integer, nullable=True)  # Duration (in seconds)
    
    # One-to-Many relationship with VideoData
    statistics_series: Mapped[list["VideoStatistics"]] = relationship("VideoStatistics", cascade="all, delete-orphan")

class VideoStatistics(Base):
    '''비디오별 시계열 통계 정보'''
    __tablename__ = "video_statistics_series"
    
    video_id: Mapped[str] = mapped_column(String, ForeignKey("video_metadata.video_id"), primary_key=True, index=True)  # YouTube VIDEO_ID
    crawl_time: Mapped[datetime] = mapped_column(DateTime, primary_key=True, index=True)  # Crawl Time
    views: Mapped[int] = mapped_column(Integer, default=0)  # Views
    likes: Mapped[int] = mapped_column(Integer, default=0)  # Likes
    comments: Mapped[int] = mapped_column(Integer, default=0)  # Comments
    