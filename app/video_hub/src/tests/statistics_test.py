from datetime import datetime
from typing import Any
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlmodel.pool import StaticPool
from models import Video, VideoStatistics
import requests

@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "postgresql://test:test1!@localhost:5433/test", poolclass=StaticPool
    )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        #TODO video와 video_statistics에 API 테스트를 위한 더미 데이터 추가
        yield session  
        #TODO 추가했던 더미 데이터 삭제

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_db] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()  

@pytest.fixture(scope="module")
def admin_token():
    response = requests.post("http://localhost:9999/login", json={"username": "pyler", "password": "pyler1!"})
    assert response.status_code == 200
    return response.json().get("access_token")

@pytest.fixture(scope="module")
def user_token():
    response = requests.post("http://localhost:9999/login", json={"username": "simon", "password": "simon"})
    assert response.status_code == 200
    return response.json().get("access_token")

# 여러 비디오와 통계 데이터를 추가하는 테스트용 Fixture
@pytest.fixture(name="multiple_videos_data")
def multiple_videos_data_fixture(session:Session):
    # 첫 번째 비디오와 통계 데이터
    video1 = Video(
        video_id="video_1",
        title="비디오 1",
        description="테스트용 비디오 1",
        upload_time=datetime(2023, 11, 1, 0, 0, 0),
        thumbnail="http://example.com/thumbnail1.jpg",
        channel_id="channel1",
        category_id=10,
        duration=600,
    )
    statistics1_1 = VideoStatistics(
        video_id=video1.video_id,
        crawl_time=datetime(2023, 11, 1, 1, 0, 0),
        views=100,
        likes=10,
        comments=5,
    )
    statistics1_2 = VideoStatistics(
        video_id=video1.video_id,
        crawl_time=datetime(2023, 11, 2, 1, 0, 0),
        views=150,
        likes=15,
        comments=8,
    )
    
    # 두 번째 비디오와 통계 데이터
    video2 = Video(
        video_id="video_2",
        title="비디오 2",
        description="테스트용 비디오 2",
        upload_time=datetime(2023, 11, 1, 0, 0, 0),
        thumbnail="http://example.com/thumbnail2.jpg",
        channel_id="channel2",
        category_id=20,
        duration=300,
    )
    statistics2_1 = VideoStatistics(
        video_id=video2.video_id,
        crawl_time=datetime(2023, 11, 1, 1, 0, 0),
        views=200,
        likes=20,
        comments=10,
    )
    statistics2_2 = VideoStatistics(
        video_id=video2.video_id,
        crawl_time=datetime(2023, 11, 2, 1, 0, 0),
        views=250,
        likes=25,
        comments=12,
    )

    session.add_all([video1, video2, statistics1_1, statistics1_2, statistics2_1, statistics2_2])
    session.commit()

    yield [video1, video2], [statistics1_1, statistics1_2, statistics2_1, statistics2_2]

    # 테스트 후 데이터 삭제
    session.delete(statistics1_1)
    session.delete(statistics1_2)
    session.delete(statistics2_1)
    session.delete(statistics2_2)
    session.delete(video1)
    session.delete(video2)
    session.commit()

# 개별 비디오에 대한 통계 시리즈 테스트
def test_get_statistics_series_for_multiple_videos(client: TestClient, multiple_videos_data:Any, user_token:str):
    videos, statistics = multiple_videos_data

    # 첫 번째 비디오의 통계 시리즈 가져오기
    response = client.get(
        "/statistics/series",
        headers={"Authorization": f"Bearer {user_token}"},
        params={
            "video_id": videos[0].video_id,
            "from_datetime": "2023-11-01T00:00:00",
            "to_datetime": "2023-11-02T23:59:59"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # 통계 시리즈가 두 개 있어야 함
    assert data[0]["views"] == statistics[0].views
    assert data[1]["likes"] == statistics[1].likes

# 특정 비디오에 대한 기간별 통계 추세 테스트
def test_get_statistics_trends_for_multiple_videos(client: TestClient, multiple_videos_data:Any, user_token:str):
    videos, statistics = multiple_videos_data

    # 첫 번째 비디오의 통계 추세 가져오기
    response = client.get(
        f"/statistics/trends/{videos[0].video_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        params={
            "from_datetime": "2023-11-01T00:00:00",
            "to_datetime": "2023-11-02T23:59:59"
        }
    )
    assert response.status_code == 200
    data = response.json()["changes"]
    assert data["views_change"] == statistics[1].views - statistics[0].views
    assert data["likes_change"] ==  statistics[1].likes - statistics[0].likes
    assert data["comments_change"] == statistics[1].comments - statistics[0].comments

# 전체 비디오에 대한 기간별 통계 추세 테스트
def test_get_total_statistics_trends_for_multiple_videos(client: TestClient, multiple_videos_data:Any, user_token:str):
    _, statistics = multiple_videos_data

    response = client.get(
        "/statistics/trends",
        headers={"Authorization": f"Bearer {user_token}"},
        params={
            "from_datetime": "2023-11-01T00:00:00",
            "to_datetime": "2023-11-02T23:59:59"
        }
    )
    assert response.status_code == 200
    data = response.json()["changes"]
    assert data["views_change"] == statistics[1].views - statistics[0].views + statistics[3].views - statistics[2].views
    assert data["likes_change"] ==  statistics[1].likes - statistics[0].likes + statistics[3].likes - statistics[2].likes
    assert data["comments_change"] == statistics[1].comments - statistics[0].comments + statistics[3].comments - statistics[2].comments