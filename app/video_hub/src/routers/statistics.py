
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import TotalVideoStatisticsResponse, VideoStatisticsResponse, VideoStatisticsSeriesResponse
import utils.auth as auth
from cores.statistics import get_statistics_series_for_video, get_statistics_trends_for_video, get_total_statistics_trends

router = APIRouter(tags=["Statistics"])

@router.get("/statistics/series", response_model=List[VideoStatisticsSeriesResponse])
def get_statistics_series_for_video_entry(
    video_id: str | None = Query(None), 
    from_datetime: datetime | None = Query(None, example="2024-01-01T00:00:00"), 
    to_datetime: datetime | None = Query(None, example="2024-01-31T23:59:59"), 
    current_user: str = Depends(auth.verify_user_role), 
    db: Session = Depends(get_db)
):
    result = get_statistics_series_for_video(video_id, from_datetime, to_datetime, db)
    return result


@router.get("/statistics/trends/{video_id}", response_model=VideoStatisticsResponse)
def get_statistics_trends_for_video_entry(
    video_id: str,
    from_datetime: datetime = Query(..., example="2024-01-01T00:00:00"),
    to_datetime: datetime = Query(..., example="2024-01-31T23:59:59"),
    current_user: str = Depends(auth.verify_user_role),
    db: Session = Depends(get_db)
):
    result = get_statistics_trends_for_video(video_id, from_datetime, to_datetime, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 기간에 대한 통계가 없음")
    return result


@router.get("/statistics/trends", response_model=TotalVideoStatisticsResponse)
def get_total_statistics_trends_entry(
    from_datetime: datetime = Query(..., example="2024-01-01T00:00:00"),
    to_datetime: datetime = Query(..., example="2024-01-31T23:59:59"),
    current_user: str = Depends(auth.verify_user_role),
    db: Session = Depends(get_db)
):
    result = get_total_statistics_trends(from_datetime, to_datetime, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 기간에 대한 통계가 없음")
    return result