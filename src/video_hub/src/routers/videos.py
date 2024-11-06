from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Video
from schemas import VideoCreate, VideoResponse
import utils.auth as auth
from cores.videos import create_video, get_video_details, delete_video, get_all_videos
from cores.exceptions import NotFoundException, InvalidURLFormatException, AlreadyExistsException
from task import insert_video_statistics

router = APIRouter(tags=["Videos"])

# Video Management Endpoints
@router.post("/videos", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video_entry(video: VideoCreate, current_user: str = Depends(auth.verify_admin_role), db: Session = Depends(get_db)):
    ''' 비디오 추가 '''
    result : Video
    try:
        result = create_video(video, db)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidURLFormatException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except AlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return result


@router.get("/videos", response_model=List[VideoResponse])
def get_all_videos_entry(current_user: str = Depends(auth.verify_user_role), db: Session = Depends(get_db)):
    '''모든 비디오 정보 조회'''
    return get_all_videos(db)


@router.get("/videos/{video_id}", response_model=VideoResponse)
def get_video_details_entry(video_id: str, current_user: str = Depends(auth.verify_user_role), db: Session = Depends(get_db)):
    '''비디오 상세 정보 조회'''
    result: Video | None = get_video_details(video_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DB에 비디오 정보 없음")
    return result


@router.delete("/videos/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video_entry(video_id: str, current_user: str = Depends(auth.verify_admin_role), db: Session = Depends(get_db)):
    '''비디오 삭제'''
    try:
        delete_video(video_id, db)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return None


@router.post("/task", status_code=status.HTTP_200_OK)
async def trigger_update_task(current_user: str = Depends(auth.verify_admin_role), db: Session = Depends(get_db)):
    ''' 통계 업데이트 태스크 트리거 '''
    await insert_video_statistics(db)
    return None