from django.urls import path
from .views import notifications,mark_notification_as_read,delete_notification,mark_all_as_read,delete_all_read

urlpatterns = [
    path("", notifications, name = "notifications"),
    path("mark-as-read/<str:id>/", mark_notification_as_read, name = "mark-as-read"),
    path("delete-notification/<str:id>/",delete_notification,name = "delete-notification"),
    path("mark-all-as-read/", mark_all_as_read, name = "mark-all-as-read"),
    path("delete-all-read/", delete_all_read, name = "delete-all-read")
]