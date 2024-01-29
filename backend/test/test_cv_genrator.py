from fastapi.testclient import TestClient
from app import app, send_response
from unittest.mock import patch, Mock
from config import CONFIG
from langchain.callbacks import AsyncIteratorCallbackHandler


client = TestClient(app)

def test_error_response():
    response = client.post(
        "/CvGen/",
        data="resume=test4&position=test4&words=10&jd=test4&additional_instructions=",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
    

def test_ok_response():
    response = client.post(
        "/CvGen/",
        data="resume=test4&position=test4&words=10&jd=test4&additional_instructions=",
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert response.text != ""
    
