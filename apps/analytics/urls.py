from django.urls import path

from apps.analytics.views import LikeAnalyticsAPIView, UserActivityAPIView

urlpatterns = [
    path("like/", LikeAnalyticsAPIView.as_view(), name="like-analytics"),
    path("user-activity/<int:id>/", UserActivityAPIView.as_view(), name="user-activity"),

]

app_name = "analytics"
