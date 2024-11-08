from django.urls import path
from . import views

urlpatterns = [
    path('', views.func_get, name='func_get'), # GET запрос
    path('submit/', views.func_post, name='func_post'), # POST запрос (куда будет отправляться форма)
]
