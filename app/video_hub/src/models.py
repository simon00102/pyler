from datetime import datetime
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Video(Base):
    '''비디오 메타 데이터 정보'''
    __tablename__ = "video_metadata"

    video_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)  # YouTube VIDEO_ID
    title: Mapped[str] = mapped_column(String, nullable=True)  # 제목
    description: Mapped[str] = mapped_column(String, nullable=True)  # 설명
    upload_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # 업로드 시간
    thumbnail: Mapped[str] = mapped_column(String, nullable=True)  # 썸네일 URL
    channel_id: Mapped[str] = mapped_column(String, nullable=True)  # 채널 ID
    category_id: Mapped[int] = mapped_column(Integer, nullable=True)  # 카테고리 ID
    duration: Mapped[int] = mapped_column(Integer, nullable=True)  # 길이 (초 단위)
    
    # VideoStatistics와 일대다 관계, 부모가 삭제되면 자식도 자동 삭제
    statistics_series: Mapped[list["VideoStatistics"]] = relationship(
        "VideoStatistics", 
        back_populates="video",
        cascade="all, delete-orphan"
    )

class VideoStatistics(Base):
    '''비디오별 시계열 통계 정보'''
    __tablename__ = "video_statistics_series"
    
    video_id: Mapped[str] = mapped_column(String, ForeignKey("video_metadata.video_id", ondelete="CASCADE"), primary_key=True, index=True)  # YouTube VIDEO_ID
    crawl_time: Mapped[datetime] = mapped_column(DateTime, primary_key=True, index=True)  # 크롤 시간
    views: Mapped[int] = mapped_column(Integer, default=0)  # 조회수
    likes: Mapped[int] = mapped_column(Integer, default=0)  # 좋아요
    comments: Mapped[int] = mapped_column(Integer, default=0)  # 댓글 수

    # Video와 관계 설정
    video: Mapped[Video] = relationship("Video", back_populates="statistics_series")
