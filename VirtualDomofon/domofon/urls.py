from django.urls import path
from .views import DomofonStatusView, DomofonControlView

urlpatterns = [
    path('status/', DomofonStatusView.as_view(), name='domofon_status'),
    path('control/', DomofonControlView.as_view(), name='domofon_control'),
]