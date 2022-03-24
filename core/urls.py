from django.urls import path

from core.views import S3ConfigView

app_name = "core"

urlpatterns = [
    path("api/", S3ConfigView.as_view(), name="config")
]
