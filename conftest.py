import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Category, Post


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="test_user", password="test_password")


@pytest.fixture
def test_category(db):
    return Category.objects.create(name="test category")


@pytest.fixture
def test_post(test_category):
    return Post.objects.create(
        title="Test post",
        text="This is a testing post.",
        pub_date=timezone.now(),
        category=test_category,
    )
