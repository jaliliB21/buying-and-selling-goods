from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('', views.Items.as_view(), name='items'),
     path('<int:pk>/', views.Detail.as_view(), name='detail'),
    path('<int:pk>/edit/', views.Edit.as_view(), name='edit'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='delete'),
    path('new/', views.New.as_view(), name='new'),
]