# 파일러 과제
전체 아키텍처 이미지?

전체 구현 Stack: Python, FastAPI, SQLAlchemy, Postgresql

## 서비스 설명
### 1. 인증/인가 서버
유저에 대한 인증 및 Access Token 발급. 현재는 admin/user 권한만 존재함.

user는 video_hub 서비스의 동영상 조회만 가능. -> sampleuser, simon
admin은 video_hub 서비스의 동영상 추가, 삭제도 가능. -> pyler

#### API List
1. 회원 가입
2. 로그인
3. \[관리자\]권한 추가 (수정, 삭제 미구현)

#### 테이블
1. 유저 마스터
2. 권한 마스터
3. 유저 - 권한 M:M

### 2. 비디오 허브 API 서버

### 3. 비디오 정보 수집 비동기 태스크 서버

## 실행 방법

## 필요 자료
1. 소스코드
2. Database Initializer
3. API Doc
4. DB ERD
5. readme.md


## Minor Issue Note
passlib deprecated 되어 최신 bcrypt와 호환 안됨. 버전 맞춰줘야 함.