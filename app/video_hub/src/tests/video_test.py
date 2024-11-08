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

# Test setup to add dummy data for Video and VideoStatistics
@pytest.fixture(name="video_data")
def video_data_fixture(session: Session):
    video = Video(
        video_id="test_video_123",
        title="Test Video",
        description="A sample video for testing",
        upload_time="2023-11-01T00:00:00",
        thumbnail="http://example.com/thumbnail.jpg",
        channel_id="channel123",
        category_id=10,
        duration=600,
    )
    session.add(video)
    session.commit()
    yield video
    session.delete(video)
    session.commit()

@pytest.fixture(name="video_statistics_data")
def video_statistics_data_fixture(session: Session, video_data: Video):
    video_statistics = VideoStatistics(
        video_id=video_data.video_id,
        crawl_time="2023-11-01T01:00:00",
        views=100,
        likes=10,
        comments=5,
    )
    session.add(video_statistics)
    session.commit()
    yield video_statistics
    session.delete(video_statistics)
    session.commit()

# Video API Tests
def test_add_video(session:Session, client: TestClient, admin_token :str):
    response = client.post(
        "/videos",
        json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    response = client.post(
        "/videos",
        json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 409
    session.query(Video).filter(Video.video_id == "jNQXAC9IVRw").delete()
    session.commit()

def test_retrieve_videos(client: TestClient, video_data:Video, user_token:str):
    response = client.get("/videos", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert any(video["video_id"] == video_data.video_id for video in response.json())

def test_retrieve_specific_video(client: TestClient, video_data:Video, user_token:str):
    response = client.get(f"/videos/{video_data.video_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["video_id"] == video_data.video_id

def test_delete_video(client: TestClient, video_data:Video, admin_token:str):
    response = client.delete(f"/videos/{video_data.video_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204

def test_delete_video_unauthorized(client: TestClient, video_data:Video, user_token:str):
    response = client.delete(f"/videos/{video_data.video_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 403  # User should not be able to delete videos

def test_admin_permissions_required_for_adding_video(client: TestClient, user_token:str):
    response = client.post(
        "/videos",
        json={"videoUrl": "https://www.youtube.com/watch?v=abcdefghijk"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Only admins should be able to add videos

