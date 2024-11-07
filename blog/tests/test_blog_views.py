import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home(client):
    response = client.get(reverse("blog:home"))

    assert response.status_code == 200
    assert b"Hello, World!" in response.content


@pytest.mark.django_db
def test_category(client, test_category):
    url = reverse("blog:category", args=[test_category.id])
    response = client.get(url)

    assert response.status_code == 200
    assert b"test category" in response.content


@pytest.mark.django_db
def test_detail(client, test_user, test_post):
    test_post.likes.add(test_user)
    url = reverse("blog:detail", args=[test_post.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["total_likes"] == test_post.total_likes()
    assert test_post.title in response.content.decode()
