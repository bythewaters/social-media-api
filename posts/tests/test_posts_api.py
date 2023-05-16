from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from posts.models import Post
from posts.serializers import PostSerializer
from profiles.models import Profile

POST_URL = reverse("posts:post_list-list")
POST_CREATE_URL = reverse("posts:create_post-list")
MY_POSTS_URL = reverse("posts:post_list-my-posts")
FOLLOWERS_POSTS_URL = reverse("posts:post_list-following-users-posts")
PROFILE_URL = reverse("profiles:profiles_list-list")


def sample_post(**params):
    defaults = {
        "title": "test_title",
        "content": "test_content",
        "owner": None,
    }
    defaults.update(params)

    return Post.objects.create(**defaults)


def sample_profile(**params):
    defaults = {
        "user": None,
        "username": "TestUsername",
        "first_name": "Test",
        "last_name": "test",
        "bio": "testbio",
        "location": "Testlocation",
    }
    defaults.update(params)

    return Profile.objects.create(**defaults)


class UnauthenticatedPostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatePostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass",
        )
        self.user2 = get_user_model().objects.create_user(
            "test2@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user1)

    def test_list_post(self):
        sample_post(owner=self.user1)
        sample_post(owner=self.user2)

        res = self.client.get(POST_URL)

        profiles = Post.objects.order_by("id")
        serializer = PostSerializer(profiles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_post(self):
        payload = {
            "title": "test_title",
            "content": "test_content",
            "created_time": timezone.now().strftime("%Y-%m-%dT%H:%M"),
            "owner": self.user1,
        }
        res = self.client.post(POST_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_my_posts(self):
        post1 = sample_post(owner=self.user1)
        post2 = sample_post(owner=self.user2)

        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        res = self.client.get(MY_POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_following_user_posts(self):
        sample_profile(user=self.user1)
        user2 = sample_profile(user=self.user2, username="test31")
        post1 = sample_post(owner=self.user1)
        post2 = sample_post(owner=self.user2)
        self.client.get(PROFILE_URL + f"{user2.id}/follow/")
        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        res = self.client.get(FOLLOWERS_POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer1.data, res.data)

    def test_add_comment_in_post(self):
        post2 = sample_post(owner=self.user2)
        comment_data = {"content": "Test Comment"}
        serializer2 = PostSerializer(post2)
        res = self.client.post(POST_URL + f"{post2.id}/add-comment/", data=comment_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer2.data["comments"], 1)

    def test_like_post(self):
        post1 = sample_post(owner=self.user1)
        serializer2 = PostSerializer(post1)
        self.assertEqual(serializer2.data["likes_count"], 0)
        res = self.client.post(POST_URL + f"{post1.id}/like/")

        post1.refresh_from_db()
        serializer2 = PostSerializer(post1)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(serializer2.data["likes_count"], 1)

    def test_dislike_post(self):
        post1 = sample_post(owner=self.user1)
        serializer2 = PostSerializer(post1)
        self.assertEqual(serializer2.data["dislikes_count"], 0)
        res = self.client.post(POST_URL + f"{post1.id}/dislike/")

        post1.refresh_from_db()
        serializer2 = PostSerializer(post1)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(serializer2.data["dislikes_count"], 1)

    def test_delete_like_if_add_dislike(self):
        post1 = sample_post(owner=self.user1)
        PostSerializer(post1)
        self.client.post(POST_URL + f"{post1.id}/like/")

        post1.refresh_from_db()
        serializer2 = PostSerializer(post1)
        self.assertEqual(serializer2.data["likes_count"], 1)

        self.client.post(POST_URL + f"{post1.id}/dislike/")
        post1.refresh_from_db()
        serializer2 = PostSerializer(post1)
        self.assertEqual(serializer2.data["likes_count"], 0)
        self.assertEqual(serializer2.data["dislikes_count"], 1)
