# 파일러 과제
전체 아키텍처 이미지?
## 서비스 설명
### 1. 인증/인가 서버
공통으로 활용되는 서비스

#### 필요한 API List
1. 회원 가입
2. 로그인
3. 권한 조회
4. ??권한 추가/삭제/수정??

#### 테이블
1. 유저 마스터
2. 권한 마스터
3. 유저 - 권한

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