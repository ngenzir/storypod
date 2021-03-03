from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Story
# Create your tests here.
User = get_user_model()

class StoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
        Story.objects.create(content="my first story", 
            user=self.user)
        Story.objects.create(content="my first story", 
            user=self.user)
        Story.objects.create(content="my first story", 
            user=self.userb)
        self.currentCount = Story.objects.all().count()

    def test_story_created(self):
        story_obj = Story.objects.create(content="my second story", 
            user=self.user)
        self.assertEqual(story_obj.id, 4)
        self.assertEqual(story_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='apassword')
        return client
    
    def test_story_list(self):
        client = self.get_client()
        response = client.get("/api/stories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_story_list(self):
        client = self.get_client()
        response = client.get("/api/stories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
    
    def test_stories_related_name(self):
        user = self.user
        self.assertEqual(user.stories.count(), 2)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/stories/action/", 
            {"id": 1, "action": "like"})
        like_count = response.json().get("likes")
        user = self.user
        my_like_instances_count = user.storylike_set.count()
        my_related_likes = user.story_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances_count, 1)
        self.assertEqual(my_like_instances_count, my_related_likes)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/stories/action/", 
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/stories/action/", 
            {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_restory(self):
        client = self.get_client()
        response = client.post("/api/stories/action/", 
            {"id": 2, "action": "restory"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_story_id = data.get("id")
        self.assertNotEqual(2, new_story_id)
        self.assertEqual(self.currentCount + 1, new_story_id)

    def test_story_create_api_view(self):
        request_data = {"content": "My test story"}
        client = self.get_client()
        response = client.post("/api/stories/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_story_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_story_id)
    
    def test_story_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/story/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_story_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/stories/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/stories/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/stories/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)