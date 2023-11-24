from django.urls import path

from apps.analytics.views import LikeAnalyticsAPIView

urlpatterns = [
    path("like/", LikeAnalyticsAPIView.as_view(), name="like-analytics"),

]

app_name = "analytics"
