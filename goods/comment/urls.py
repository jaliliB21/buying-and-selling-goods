from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('items/<int:pk>/', views.ShowAllCommentsItem.as_view(), name='comments')
]