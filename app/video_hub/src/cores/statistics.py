from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import VideoStatistics
from schemas import TotalVideoStatisticsResponse, VideoStatisticsChange, VideoStatisticsResponse

def get_statistics_series_for_video(
    video_id: str | None,
    from_datetime: datetime | None,
    to_datetime: datetime | None,
    db: Session
):
    query = db.query(VideoStatistics)
    
    if video_id:
        query = query.filter(VideoStatistics.video_id == video_id)

    if from_datetime:
        query = query.filter(VideoStatistics.crawl_time >= from_datetime)

    if to_datetime:
        query = query.filter(VideoStatistics.crawl_time <= to_datetime)
    
    return query.all()

def get_statistics_trends_for_video(video_id: str, from_datetime: datetime, to_datetime: datetime, db: Session):
    sql_query = text("""
        WITH start_data AS (
            SELECT * FROM video_statistics_series
            WHERE video_id = :video_id
            AND crawl_time >= :from_datetime
            AND crawl_time <= :to_datetime
            ORDER BY crawl_time ASC
            LIMIT 1
        ),
        end_data AS (
            SELECT * FROM video_statistics_series
            WHERE video_id = :video_id
            AND crawl_time >= :from_datetime
            AND crawl_time <= :to_datetime
            ORDER BY crawl_time DESC
            LIMIT 1
        )
        SELECT
            end_data.views - start_data.views AS views_change,
            end_data.likes - start_data.likes AS likes_change,
            end_data.comments - start_data.comments AS comments_change,
            start_data.crawl_time AS start_time,
            end_data.crawl_time AS end_time
        FROM start_data, end_data;
    """)

    result = db.execute(sql_query, {
        "video_id": video_id,
        "from_datetime": from_datetime,
        "to_datetime": to_datetime
    }).mappings().first()

    if not result:
        return None

    return VideoStatisticsResponse(
        video_id=video_id,
        from_datetime=from_datetime,
        to_datetime=to_datetime,
        changes=VideoStatisticsChange(
            views_change=result["views_change"],
            likes_change=result["likes_change"],
            comments_change=result["comments_change"]
        ),
        start_time=result["start_time"],
        end_time=result["end_time"]
    )

def get_total_statistics_trends(from_datetime: datetime, to_datetime: datetime, db: Session):
    sql_query = text("""
        WITH start_data AS (
            SELECT video_id, views, likes, comments, crawl_time,
                ROW_NUMBER() OVER (PARTITION BY video_id ORDER BY crawl_time ASC) AS row_num
            FROM video_statistics_series
            WHERE crawl_time >= :from_datetime
            AND crawl_time <= :to_datetime
        ),
        end_data AS (
            SELECT video_id, views, likes, comments, crawl_time,
                ROW_NUMBER() OVER (PARTITION BY video_id ORDER BY crawl_time DESC) AS row_num
            FROM video_statistics_series
            WHERE crawl_time >= :from_datetime
            AND crawl_time <= :to_datetime
        )
        SELECT 
            SUM(end_data.views - start_data.views) AS views_change,
            SUM(end_data.likes - start_data.likes) AS likes_change,
            SUM(end_data.comments - start_data.comments) AS comments_change
        FROM start_data
        JOIN end_data ON start_data.video_id = end_data.video_id
        WHERE start_data.row_num = 1 AND end_data.row_num = 1;
    """)

    result = db.execute(sql_query, {
        "from_datetime": from_datetime,
        "to_datetime": to_datetime
    }).mappings().first()

    if result is None or result["views_change"] is None:
        return None

    return TotalVideoStatisticsResponse(
        from_datetime=from_datetime,
        to_datetime=to_datetime,
        changes=VideoStatisticsChange(
            views_change=result["views_change"],
            likes_change=result["likes_change"],
            comments_change=result["comments_change"]
        )
    )