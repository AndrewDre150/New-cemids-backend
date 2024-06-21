# profiles/urls.py

from django.urls import path
from .views import UserProfileListCreateView, UserProfileDetailView

urlpatterns = [
    path('api/profiles/', UserProfileListCreateView.as_view(), name='profile-list-create'),
    path('api/profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
]
