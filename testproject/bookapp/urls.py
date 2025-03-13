from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='home'),
    path('create', views.create, name='create'),
    path('update/<int:pk>', views.BookUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete'),
    path('register', views.register, name='register'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.custom_logout, name='logout'),
]
