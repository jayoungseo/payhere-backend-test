# [페이히어] Python 백엔드 엔지니어 과제
이름: 서자영
email: tjwkdud0423@gmail.com

---
## Install
~~~
$ pip install -r requirements.txt
~~~
## 환경변수
아래와 같은 .env 파일을 만들어 저장해주세요
(SECRET_KEY는 `openssl rand -hex 32` 로 생성가능)

```
TZ=Asia/Seoul
DB_HOST=
DB_PORT=
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=

API_DOMAIN_ADDRESS=localhost:8000

SECRET_KEY=607a29ba4e5ede8e30a55cbfed07d632d5f3dab4603b047976253b727aad1d4f
```
## Run
DB 실행
```
docker-compose up -d
```
FastAPI 실행
```
uvicorn service.main:app --reload
```

---
## Database ERD
![db_erd_image](/readme_img/ERD_image.jpg)

## API 리스트


|API 주소|method|token 인증|설명|요청/반환값|
|---|---|---|---|---|
|/signup|POST|N|회원가입|[보기](/readme_img/signup.png)|
|/login|POST|N|로그인|[보기](/readme_img/login.png)|
|/token|POST|N|새로운 access token 발급|[보기](/readme_img/token.png)|
|/logout|POST|Y|로그아웃|[보기](/readme_img/logout.png)|
||||||
||||||
|/account-book|GET|Y|사용자가 작성한 모든 세부내역 조회|[보기](/readme_img/get_all_account.png)|
|/account-book|POST|Y|세부내역 작성|[보기](/readme_img/write_account.png)|
|/account-book/{id}|GET|Y|하나의 세부내역 조회|[보기](/readme_img/get_one_account.png)|
|/account-book/{id}/share-url|GET|Y|세부내역 공유위한 단축url 생성|[보기](/readme_img/share_url.png)|
|/account-book/{id}/update|POST|Y|세부내역 수정|[보기](/readme_img/update_account.png)|
|/account-book/{id}/copy|POST|Y|세부내역 복제|[보기](/readme_img/copy_account.png)|
|/account-book/{id}/delete|POST|Y|세부내역 삭제|[보기](/readme_img/delete_account.png)|
|||||||
||||||
|/url/{code}|GET|N|공유 url 접근시 세부내역 보여줌|[보기](/readme_img/url_code.png)|

### Curl 예시
- token 인증 필요없는 경우
~~~bash
curl -X 'POST' \
  'http://localhost:8000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string"
}'
~~~
- token 인증 필요한 경우
~~~bash
curl -X 'POST' \
  'http://localhost:8000/account-book' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQzNTA3NzksInVzZXJfaWQiOjF9.XN1QwYstj0pzZ_moRM_9XFbKzvuI32X5QrypIpOOxmk' \
  -d '{
  "amount": 10000,
  "memo": "shopping"
}'
~~~
---


## 요구사항 확인하기

1. 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다. 
    >- `POST /signup` [코드 보기](/service/router/login.py)
    
2. 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다.
    >- `POST /login`, `POST /logout` [코드 보기](/service/router/login.py)
    >- 로그인 성공시 access_token, refresh_token 반환
    >- 로그아웃시 refresh_token 삭제

3. 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다. 
    1. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
        >- `POST /account-book` [코드 보기](/service/router/account.py)
        >- 보통 가계부를 생각하면 하나의 내역 관련해서 금액, 수입/지출, 카테고리, 메모 등 많은 입력값이 있지만 `오늘 사용한 돈의 금액과 관련된 메모`라고 했기때문에 간단히 금액과, 메모 2가지를 입력받는것으로 함

    2. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다. 
        >- `POST /account-book/{id}/update` [코드 보기](/service/router/account.py)
        >- 금액, 메모 수정 가능

    3. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
        >- `POST /account-book/{id}/delete` [코드 보기](/service/router/account.py)
        >- 복구 가능성 때문에 바로 DB에서 삭제하지 않고 is_deleted 컬럼을 만들어 삭제 여부를 구분함 (0: 존재, 1: 삭제)

    4. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
        >- `GET /account-book` [코드 보기](/service/router/account.py)
        >- 삭제된 세부 내역을 제외한 모든 내역 정보 반환

    5. 가계부에서 상세한 세부 내역을 볼 수 있습니다.
        >- `GET /account-book/{id}` [코드 보기](/service/router/account.py)
        >- 하나의 세부 내역 정보 반환, 삭제된 내역은 보이지 않음

    6. 가계부의 세부 내역을 복제할 수 있습니다.
        >- `POST /account-book/{id}/copy` [코드 보기](/service/router/account.py)
        >- 세부 내역 복제시 똑같은 세부 내역(금액, 메모) 정보가 하나가 더 DB에 추가된다고 생각함

    7. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
        (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
        >- `GET /account-book/{id}/copy` [코드 보기](/service/router/account.py)
        >- base62 인코딩 방식으로 단축 url을 생성해서 반한함
        >- 반환값의 도메인 부분은 띄워진 서버에 따라 수정해야함
        >- 단축 url 접근시 만료 날짜 컬럼 비교 후 만료되지 않은 경우에만 내용 반환함 [코드 보기](/service/router/url.py)

로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.
>- [코드 보기](/service/router/depends.py)
>- 가계부에 관련된 api는 모두 헤더에 입력된 토큰을 검증하게 되어있음
>- 로그인하지 않은 고객은 가계부 정보 조회 불가능
>- 단축 url로 공유된 링크 접근시 만료 시간 전까지는 로그인 하지 않은 사용자도 내용 보기 가능

---

## 구현 확인하기
- DB 관련 테이블에 대한 DDL 파일을 소스 디렉토리 안에 넣어주세요.
    >- [코드 보기](/service/models.py)

- 가능하다면 테스트 케이스를 작성해주세요.
    >- [코드 보기](/test_main.py)
    >- 테스트 코드는 처음 작성해봐서 제대로 구현하지 못했음
    >- 생성 날짜/시간이 반환되는 api는 테스트 코드 작성하는데 어려움이 있어 구현하지 못함

- 별도의 요구사항이 없는 것은 지원자가 판단해서 개발합니다.

- JWT 토큰을 발행해서 인증을 제어하는 방식으로 구현해주세요
    >- jwt 토큰 발급 흐름 ![jwt_token_flow](/readme_img/jwt_token_flow.jpg)
    >- access_token 검증 [코드 보기](/service/router/depends.py)
    >- 새로운 access_token 발급 `POST /token` [코드 보기](/service/router/login.py)

- 비밀번호는 암호화되어 저장되어야 합니다.
    >- [코드 보기](/service/core/security.py)
    >- 모든 비밀번호는 해싱처리되어 저장됨
    >- user 테이블 예시 ![db_erd_image](/readme_img/user_table_sample.jpg)
