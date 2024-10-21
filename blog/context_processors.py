from blog.models import Category

def category_menu(request):
    return {
        "category_menu": Category.objects.all().order_by("name")
    }