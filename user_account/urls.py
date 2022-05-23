from django.urls import path
from .views import account_page, profile, create_profile, update_profile, delete_profile, follow, unfollow, my_followers, following

urlpatterns = [
    path("",account_page,name = "my-account"),
    path("my-followers/<str:id>/",my_followers,name = "followers"),
    path("following/<str:id>/", following, name  = "following"),

    # profile urls
    path("profile/create",create_profile,name = "create-profile"),
    path("profile/update/",update_profile,name = "update-profile"),
    path("profile/delete/",delete_profile,name = "delete-profile"),
    path("profile/<str:id>/",profile,name = "profile"),

    #follow urls
    path("follow/<int:id>/", follow, name = "follow"),
    path("unfollow/<int:id>/", unfollow, name = "unfollow")
]