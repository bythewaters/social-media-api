import os
import tempfile

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from profiles.models import Profile
from profiles.serializers import ProfileListSerializer, UpdateProfileSerializer

PROFILE_URL = reverse("profiles:profiles_list-list")
PROFILE_CREATE_URL = reverse("profiles:create_profile-list")
MY_PROFILE_URL = reverse("profiles:my_profile-list")


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


def image_upload_url():
    """Return URL for recipe image upload"""
    return reverse("profiles:my_profile-upload-image")


class UnauthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedProfileApiTests(TestCase):
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
        self.client.force_authenticate(self.user2)

    def test_list_profiles(self):
        sample_profile(user=self.user1)
        sample_profile(user=self.user2, username="testusername")

        res = self.client.get(PROFILE_URL)

        profiles = Profile.objects.order_by("id")
        serializer = ProfileListSerializer(profiles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_profiles_by_username(self):
        profile1 = sample_profile(user=self.user1)
        profile2 = sample_profile(user=self.user2, username="FindTest")

        res = self.client.get(
            PROFILE_URL, {"username": f"{profile2.username}"}
        )

        serializer1 = ProfileListSerializer(profile1)
        serializer2 = ProfileListSerializer(profile2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer1.data, res.data)

    def test_filter_profiles_by_location(self):
        profile1 = sample_profile(user=self.user1, location="test2loc")
        profile2 = sample_profile(
            user=self.user2,
            location="Testlocation",
            username="testuser"
        )

        res = self.client.get(
            PROFILE_URL, {"location": f"{profile2.location}"}
        )

        serializer1 = ProfileListSerializer(profile1)
        serializer2 = ProfileListSerializer(profile2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer1.data, res.data)

    def test_create_profile(self):
        data = {
            "user": 1,
            "username": "TestUsername",
            "first_name": "Test",
            "last_name": "test",
            "bio": "testbio",
            "location": "Testlocation",
        }
        res = self.client.post(PROFILE_CREATE_URL, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_follow_unfollow_user(self):
        user1 = sample_profile(user=self.user1)
        user2 = sample_profile(user=self.user2, username="test31")
        self.client.force_authenticate(user=self.user1)
        res = self.client.get(PROFILE_URL + f"{user2.id}/follow/")
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertTrue(user1.following.filter(id=user2.id).exists())
        self.assertTrue(user2.followers.filter(id=user1.id).exists())

        res2 = self.client.get(PROFILE_URL + f"{user2.id}/unfollow/")
        self.assertEqual(res2.status_code, status.HTTP_302_FOUND)
        self.assertFalse(
            user1.following.filter(id=user2.id).exists()
        )
        self.assertFalse(
            user2.followers.filter(id=user1.id).exists()
        )

    def test_update_profile(self):
        profile = sample_profile(user=self.user1)
        data = {"username": "AnotherUsername"}
        serializer = UpdateProfileSerializer(
            instance=profile, data=data, partial=True
        )
        serializer.is_valid()
        updated_profile = serializer.save()
        self.assertEqual(updated_profile.username, data["username"])


class ProfileImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.profile = sample_profile(user=self.user)

    def tearDown(self):
        self.profile.profile_picture.delete()

    def test_upload_image_to_profile(self):
        """Test uploading an image to profile"""
        url = image_upload_url()
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url, {"profile_picture": ntf}, format="multipart"
            )
        self.profile.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("profile_picture", res.data)
        self.assertTrue(os.path.exists(self.profile.profile_picture.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url()
        res = self.client.post(
            url, {"profile_picture": "not image"}, format="multipart"
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_url_is_shown_on_profile_list(self):
        url = image_upload_url()
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"profile_picture": ntf}, format="multipart")
        res = self.client.get(PROFILE_URL)

        self.assertIn("profile_picture", res.data[0].keys())
