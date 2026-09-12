# 本文件由 ai/generate_script.py 自动生成，并经过人工校对。
# 校对修正：AI 将「资源不存在」的状态码误写为 401 / 402，已改为 404。
import requests


def test_get_post_success():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert "userId" in data
    assert "id" in data
    assert "title" in data
    assert "body" in data


def test_get_post_not_found():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/999999")
    assert response.status_code == 404


def test_boundary_id_zero():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/0")
    assert response.status_code == 404


def test_boundary_id_negative():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/-1")
    assert response.status_code == 404


def test_boundary_id_huge_positive():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/999999999999")
    assert response.status_code == 404
