import requests
from config.settings import API_BASE_URL

def test_get_posts():
    r=requests.get(f"{API_BASE_URL}/posts")
    assert r.status_code == 200
    assert len(r.json()) ==100

def test_get_single_post():
    r=requests.get(f"{API_BASE_URL}/posts/1")
    assert r.status_code == 200
    data=r.json()
    for field in ['userId','id','title','body']:
        assert field in data
    assert data['id']==1

def test_create_post():
    payload={"title":"foo","body":"bar","userId":1}
    r=requests.post(f"{API_BASE_URL}/posts",json=payload)
    assert r.status_code == 201
    assert r.json()["title"]=='foo'

def test_delete_post():
    r=requests.delete(f"{API_BASE_URL}/posts/1")
    assert r.status_code in [200, 204]

def test_filter_comments():
    r=requests.get(f"{API_BASE_URL}/comments",params={"postId":1})
    assert r.status_code == 200
    for comment in r.json():
        assert comment["postId"]==1

def test_response():
    r=requests.get(f"{API_BASE_URL}/posts")
    assert r.status_code == 200
    assert r.elapsed.total_seconds()< 2

def test_get_nothing():
    r = requests.get(f"{API_BASE_URL}/posts/999")
    assert r.status_code == 404