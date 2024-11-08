import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from blog.forms import PostForm
from blog.models import Category, Post


@pytest.fixture
def user(db):
    return User.objects.create_user(username="test_user", password="test_password")


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(username="test_superuser", password="test_password")


@pytest.fixture
def category(db):
    return Category.objects.create(name="test category")


@pytest.fixture
def post_form(category):
    form_data = {
        "title": "Test Post",
        "text": "This is a testing post.",
        "category": category.id,
    }
    return PostForm(data=form_data)


@pytest.fixture
def post(category):
    return Post.objects.create(
        title="Test post",
        text="This is a testing post.",
        pub_date=timezone.now(),
        category=category,
    )