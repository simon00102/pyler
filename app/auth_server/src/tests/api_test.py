import pytest
from fastapi.testclient import TestClient
from auth import get_password_hash
from main import app
from database import get_db, Base
from models import User, Role
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "postgresql://test:test1!@localhost:5433/test", poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        user = User(username="testuser", password=get_password_hash("testuser"), email="test@test.com", roles=[session.query(Role).filter(Role.name == "user").first()])
        admin = User(username="testadmin", password=get_password_hash("testadmin"), email="testadmin@test.com", roles=[session.query(Role).filter(Role.name == "admin").first()])
        
        session.add(user)
        session.add(admin)
        session.commit()
        yield session  
        session.delete(user)
        session.delete(admin)
        session.commit()

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_db] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()  

@pytest.fixture
def valid_user_token(client: TestClient):
    """유효한 사용자로 로그인하여 JWT 토큰을 반환하는 fixture"""
    response = client.post("/login", json={"username": "testuser", "password": "testuser"})
    return response.json()["access_token"]

@pytest.fixture
def valid_admin_token(client: TestClient):
    """유효한 관리자 계정으로 로그인하여 JWT 토큰을 반환하는 fixture"""
    response = client.post("/login", json={"username": "testadmin", "password": "testadmin"})
    return response.json()["access_token"]


### 1. 로그인 테스트
def test_login_success(client: TestClient):
    """유효한 사용자 정보로 로그인 성공"""
    response = client.post("/login", json={"username": "testuser", "password": "testuser"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure_invalid_username(client: TestClient):
    """잘못된 사용자 이름으로 로그인 실패"""
    response = client.post("/login", json={"username": "invaliduser", "password": "testuser"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_login_failure_invalid_password(client: TestClient):
    """잘못된 비밀번호로 로그인 실패"""
    response = client.post("/login", json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_login_failure_no_password(client: TestClient):
    """정보 부족으로 실패"""
    response = client.post("/login", json={"username": "testuser"})
    assert response.status_code == 422


### 2. 권한 테스트
def test_unauthorized_access(client: TestClient):
    """인증되지 않은 사용자가 보호된 API에 접근하려고 시도할 때 접근 거부"""
    response = client.post("/assign-role")  # 인증 필요 엔드포인트
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_admin_access(valid_admin_token : str, session: Session, client: TestClient):
    """유효한 관리자 토큰을 가진 사용자가 관리자 전용 API에 접근할 수 있는지 테스트"""
    headers = {"Authorization": f"Bearer {valid_admin_token}"}
    response = client.post("/assign-role", headers=headers, json={"username": "testuser", "rolename": "admin"})
    assert response.status_code == 200  # 접근 성공

def test_user_access_denied_to_admin_api(valid_user_token : str, client: TestClient):
    """일반 사용자가 관리자 전용 API에 접근하려 할 때 접근 거부"""
    headers = {"Authorization": f"Bearer {valid_user_token}"}
    response = client.post("/assign-role", headers=headers, json={"username": "testuser", "rolename": "editor"})
    assert response.status_code == 403  # 접근 거부
    assert response.json() == {"detail": "Not enough permissions"}


### 3. 회원가입 테스트
def test_register_success(session: Session, client: TestClient):
    """새 사용자 등록 성공"""
    response = client.post("/register", json={"username": "newuser", "password": "newuser", "email": "newuser@test.com"})
    assert response.status_code == 201
    session.query(User).filter(User.username == "newuser").delete()
    session.commit()

    

def test_register_failure_existing_username(client: TestClient):
    """이미 존재하는 사용자 이름으로 등록 실패"""
    response = client.post("/register", json={"username": "testuser", "password": "testuser", "email": "test@test.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_register_failure_existing_email(client: TestClient):
    """이미 존재하는 이메일로 등록 실패"""
    response = client.post("/register", json={"username": "newuser", "password": "newuser", "email": "test@test.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

