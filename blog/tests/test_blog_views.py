import pytest
from django.urls import reverse
from blog.models import Post


@pytest.mark.django_db
def test_home(client):
    response = client.get(reverse("blog:home"))

    assert response.status_code == 200
    assert b"Hello, World!" in response.content


@pytest.mark.django_db
def test_category(client, category):
    url = reverse("blog:category", args=[category.id])
    response = client.get(url)

    assert response.status_code == 200
    assert b"test category" in response.content


@pytest.mark.django_db
def test_detail(client, user, post):
    post.likes.add(user)
    url = reverse("blog:detail", args=[post.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["total_likes"] == post.total_likes()
    assert post.title in response.content.decode()