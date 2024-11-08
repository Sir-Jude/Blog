import pytest
from blog.forms import PostForm


@pytest.mark.django_db
class TestPostForm:

    def test_post_form_validity(self, post_form):
        # Check if the form is valid
        assert post_form.is_valid()

    def test_post_form_no_category(self):
        # Create a form with no category (empty category)
        form_data = {
            "title": "Test Post without category",
            "text": "Test Content",
            "category": "",  # Empty category
        }
        form = PostForm(data=form_data)

        # Check if the form is valid
        assert form.is_valid()  # Form should be valid even with empty category
        # Call clean_category to test its behavior with no category
        cleaned_category = form.cleaned_data["category"]
        assert cleaned_category is None  # Ensure that no category is returned
