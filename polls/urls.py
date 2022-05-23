from django.urls import path
from .views import (all_polls, delete_poll, single_poll, my_polls, vote, remove_featured_poll, create_poll)

urlpatterns = [
    path("",all_polls,name = "polls"),
    path("create/",create_poll,name = "create-poll"),
    path("my-polls/",my_polls,name = "my-polls"),

    # poll functionalities path
    path("vote/",vote, name = "vote"),

    # dynamic urls
    path("<str:id>/", single_poll, name = "single-poll"),
    path("<str:id>/delete/", delete_poll, name = "delete-poll"),
    path("<str:id>/remove/", remove_featured_poll, name = "remove-featured-poll"),
]