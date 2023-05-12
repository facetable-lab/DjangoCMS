from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('category/<slug:category_slug>/', views.CategoryView.as_view(), name='category'),
]
