import pytest

from random import randint

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlmodel import Session, create_engine

from src.main import app
from src.core.database import get_session, SQLModel

BASE_URL = "/example_model"
sqlite_url = f"sqlite:///./db_test.db"
engine = create_engine(
        sqlite_url,
        echo=False,
        connect_args={"check_same_thread": False}
        )


def mock_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = mock_get_session
client = TestClient(app)


@pytest.fixture
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)



def test_connection(setup_db):
    response = client.get(BASE_URL + "/health_check")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == True


def test_create(setup_db):
    payload = {
            "name": "string",
            "favorite_number": 0,
            "date": "2024-05-15"
            }
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 200

    response_json = response.json()
    response_items = set(response_json.items())
    payload_items = set(payload.items())
    print(response_items)
    print(payload_items)
    #assert payload_items.issubset(response_items) == True
    assert payload["name"] == response_json["name"]
    assert payload["favorite_number"] == response_json["favorite_number"]
    assert payload["date"] == response_json["date"]


def test_read(setup_db):
    # ==================================================
    # create record
    payload = {
            "name": "string",
            "favorite_number": 0,
            "date": "2024-05-15"
            }
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 200

    response_json = response.json()
    response_items = set(response_json.items())
    payload_items = set(payload.items())
    assert payload_items.issubset(response_items) == True

    # ==================================================
    # check if record was created
    id = response_json["id"]
    response = client.get(BASE_URL + f"/?id={id}")

    assert response.status_code == 200

    response_json = response.json()
    response_items = set(response_json.items())
    payload_items = set(payload.items())
    assert payload_items.issubset(response_items) == True

def test_update(setup_db):
    # ==================================================
    # create record
    payload = {
            "name": "string",
            "favorite_number": 0,
            "date": "2024-05-15"
            }
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 200

    response_json = response.json()
    response_items = set(response_json.items())
    payload_items = set(payload.items())
    assert payload_items.issubset(response_items) == True

    # ==================================================
    # check if record was created
    id = response_json["id"]
    response = client.get(BASE_URL + f"/?id={id}")
    assert response.status_code == 200

    response_json = response.json()
    response_items = set(response_json.items())
    payload_items = set(payload.items())
    assert payload_items.issubset(response_items) == True

    # ==================================================
    # update record
    updated_payload = {
            "id": id,
            "name": "stringo",
            "favorite_number": 4120,
            "date": "2024-05-15"
            }
    print(updated_payload)
    response = client.post(BASE_URL + "/update", json=updated_payload)
    assert response.status_code == 200
    assert response.json() == updated_payload

def test_delete(setup_db):
    # ==================================================
    # create record
    payload = {
            "name": "string",
            "favorite_number": 0,
            "date": "2024-05-15"
            }
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 200

    response_json = response.json()
    response_items = set(response_json.items())
    payload_items = set(payload.items())
    assert payload_items.issubset(response_items) == True

    # ==================================================
    # delete created record
    id = response_json["id"]
    response = client.delete(BASE_URL + f"/?id={id}")
    assert response.status_code == 200
    assert response.json() == response_json

def test_read_all(setup_db):
    n = 0
    payload = {
            "name": f"name-{n}",
            "favorite_number": n,
            "date": "2024-05-15"
            }
    json_list = []
    for i in range(10):
        n = randint(0, 42)
        create_response = client.post(BASE_URL + "/", json=payload)
        assert create_response.status_code == 200

        create_json = create_response.json()
        response_items = set(create_json.items())
        payload_items = set(payload.items())
        assert payload_items.issubset(response_items) == True
        json_list.append(create_json)

    read_all_response = client.get(BASE_URL + "/all")
    assert read_all_response.status_code == 200
    for j in json_list:
        print(j)
        assert j in read_all_response.json(), f"{j} not inside response json"
    assert json_list == read_all_response.json()


def test_search(setup_db):
    # ==================================================
    # create record
    payload = {
            "name": "string",
            "favorite_number": 19,
            "date": "2024-05-16"
            }
    create_response = client.post(BASE_URL + "/", json=payload)
    assert create_response.status_code == 200

    create_json = create_response.json()
    response_items = set(create_json.items())
    payload_items = set(payload.items())
    assert payload_items.issubset(response_items) == True

    # ==================================================
    # check if record was created
    id = create_json["id"]
    search_response = client.get(BASE_URL + f"/search?name={payload['name']}")

    assert search_response.status_code == 200

    search_json = search_response.json()
    assert create_json in search_json, "created payload not inside search result"
