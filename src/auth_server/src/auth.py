from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Access/Refresh token을 위한 공통 함수
def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 로그인과 리프레시에서 사용할 공통 토큰 생성 함수
def generate_tokens(username: str, roles: list[str]):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_token(data={"sub": username, "roles": roles}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": username}, expires_delta=refresh_token_expires)
    
    return access_token, refresh_token
