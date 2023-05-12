from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

from .models import Category, Post


def home(request) -> HttpResponse:
    if request.method == 'GET':
        return HttpResponse('Hello')


class HomeView(View):
    """Контроллер главной страницы"""

    def get(self, request) -> render:
        context = {
            'category_qs': Category.objects.all(),
            'post_qs': Post.objects.all()
        }

        return render(request, 'blog/home.html', context)

    def post(self, request) -> HttpResponse:
        return HttpResponse('POST')


class CategoryView(View):
    """Вывод статей по категории"""

    def get(self, request, category_slug) -> render:
        context = {
            'category': Category.objects.get(slug=category_slug)
        }

        return render(request, 'blog/post_list.html', context)
