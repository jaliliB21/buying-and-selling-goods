from django.urls import path

from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.Inbox.as_view(), name='inbox'),
    path('<int:pk>/', views.Detail.as_view(), name='detail'),
    path('new/<int:item_pk>/', views.NewConversation.as_view(), name='new'),
]