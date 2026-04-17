
from django.contrib import admin
from django.urls import path, include
# path chứa 2 đối số (route và view - urls của app)
# include giúp tham chiếu tới urlsconf của app
# Luôn luôn dùng include để tham chiếu tới URL pattern ngoại trừ admin.site.urls

urlpatterns = [
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
]
