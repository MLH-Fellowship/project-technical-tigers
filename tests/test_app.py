# tests/test_app.py
from dataclasses import dataclass
import unittest 
import os
os.environ['TESTING'] = 'true'
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert "<h1 class=\"home-title\">Hello, I'm Brandon!</h1>" in html
        assert "<h3 class=\"home-subtitle\">Production Engineering Fellow</h3>" in html 

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # create a post and test if it went through
        response = self.client.post("/api/timeline_post", data = {'name' : 'John Doe', 'email' : 'john@example.com', 'content' : 'Hello!'})
        assert response.status_code == 200

        # test if we can get what was just posted
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        first_post_name = json["timeline_posts"][0]['name']
        assert first_post_name == 'John Doe'
        self.client.delete("/api/timeline_post", data = {'name' : 'John Doe'})

        # checking the timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h1 class=\"mt-3 bold-text\">TimeLine</h1>" in html
        assert "<button type=\"submit\" class=\"btn btn-primary\">Submit</button>" in html
        assert "<h3 class=\"mt-3 bold-text\">Posts</h3>" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data = {'email' : 'john@example.com', 'content' : 'Hello world, I\'m John!'})
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid name" in response_text 


        # POST request with empty content
        response = self.client.post("/api/timeline_post", data = {'name' : 'John', 'email' : 'john@example.com', 'content' : ''})
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid content" in response_text

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data = {'name' : 'John', 'email' : 'not-an-email', 'content' : 'Hello world, I\'m John!'})
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid email" in response_text