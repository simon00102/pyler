from sqlalchemy.orm import Session
from database import engine, Base
from cores.videos import fetch_video_data

def init_db():
    Base.metadata.drop_all(bind=engine)  # 테이블 삭제
    Base.metadata.create_all(bind=engine) # 테이블 생성
    
    # 샘플 데이터 추가
    with Session(engine) as session:
        create_sample_data(session)

def create_sample_data(db: Session): 

    video_list = ["HcQ4TovoWh8","h7wnMlolzT8", "5tS7mPrJ_D8", "atbMxl9E9G4", "aODhSiEI9qM"]
    for video_id in video_list:
        video, video_stats = fetch_video_data(video_id)
        db.add(video)
        db.add(video_stats)
    db.commit()
    

if __name__ == "__main__":
    init_db()
