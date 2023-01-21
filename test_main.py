from fastapi.testclient import TestClient

from service.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/signup/",
        json={
            "email": "user2@example.com",
            "password": "string"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": "user2@example.com"
    }


# 가계부 세부내역 작성 테스트
def test_write_account_book_contents():
    response = client.post(
        url="/account-book",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQzNDMwNTcsInVzZXJfaWQiOjF9.ySjhwqreY2j_WwKoGe3hrrV0KaGA0Z4hFfXUBP7kNVE"
        },
        json={
            "amount": 10000,
            "memo": "test"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "use_date": "2023-01-21",
        "amount": 10000,
        "memo": "test"
    }


# 가계부 세부내역 업데이트 테스트
def test_update_account_book_contents():
    response = client.post(
        url="/account-book/1/update",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQzNDMwNTcsInVzZXJfaWQiOjF9.ySjhwqreY2j_WwKoGe3hrrV0KaGA0Z4hFfXUBP7kNVE"
        },
        json={
            "amount": 100,
            "memo": "update success"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "use_date": "2023-01-21",
        "amount": 100,
        "memo": "update success"
    }


# 가계부 세부내역 복제 테스트
def test_copy_account_book_contents():
    response = client.post(
        url="/account-book/1/copy",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQzNDMwNTcsInVzZXJfaWQiOjF9.ySjhwqreY2j_WwKoGe3hrrV0KaGA0Z4hFfXUBP7kNVE"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "use_date": "2023-01-21",
        "amount": 100,
        "memo": "update success"
    }

