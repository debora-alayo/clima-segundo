from fastapi.testclient import TestClient
import requests
import os
from app.main import app

client = TestClient(app)
url = "https://weatherapi-com.p.rapidapi.com/current.json"
rapid_api_key = os.environ.get('RAPID_API_KEY', 'default_apikey')
rapid_api_host = os.environ.get('RAPID_API_HOST', 'default_apihost')

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Microservicio Clima :D"}

def test_get_weather():
    ciudad = "Buenos Aires"
    response = client.get(f"/weather/{ciudad}")

    assert response.status_code == 200

    assert "temperatura" in response.json()
    assert "precipitacion" in response.json()

def test_error_weather():
    ciudad = "#$%"
    response = client.get(f"/weather/{ciudad}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_header_api_key_error():
    headers = {
        "X-RapidAPI-Key": "invalid_key",
        "X-RapidAPI-Host": rapid_api_host
    } 
    querystring = {"q": "Santiago"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    assert response.status_code == 403
    assert response.json() == {"message": "You are not subscribed to this API."}

def test_header_host_error():
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "invalid_host"
    } 
    querystring = {"q": "Santiago"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    assert response.status_code == 400
    assert response.json() == {'messages': "The host you've provided is invalid. If you have difficulties, "'contact the RapidAPI support team, support@rapidapi.com'}
