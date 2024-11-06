from sqlalchemy.orm import Session
from models import Video
from schemas import VideoCreate
from cores.exceptions import AlreadyExistsException, InvalidURLFormatException, NotFoundException
from utils.youtube import fetch_video_data, extract_video_id

def create_video(video: VideoCreate, db: Session):
    '''
    Video URL에서 video_id를 추출
    video_id Youtube API를 활용해 Video와 VideoStatistics 객체를 생성하여 DB에 추가
    '''
    video_id : str | None = extract_video_id(video.video_url) #주소 형식 검증 및 id 추출.
    if(video_id is None): #주소 형식이 맞지 않음.
        raise InvalidURLFormatException("동영상 주소 형식이 맞지 않음")
    
    if(get_video_details(video_id, db)): #already exists
        raise AlreadyExistsException("이미 존재하는 동영상")
    
    video_meta, video_stat = fetch_video_data(video_id)
    if(video_meta is None or video_stat is None):
        raise NotFoundException("해당 동영상을 Youtube에서 찾을 수 없음")

    db.add(video_meta)
    db.add(video_stat)
    db.commit()

    return video_meta

def get_video_details(video_id: str, db: Session):
    result = db.query(Video).filter(Video.video_id == video_id).first()
    return result

def delete_video(video_id: str, db: Session):
    result = get_video_details(video_id, db)
    if not result:
        raise NotFoundException("해당 동영상을 찾을 수 없음")
    if result:
        db.delete(result)
        db.commit()

def get_all_videos(db: Session):
    return db.query(Video).all()