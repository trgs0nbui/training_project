from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name = "index"),
    
    path("<int:question_id>/", views.detail, name = "detail"),
    path("<int:question_id>/", views.results, name = "results"),
    path("<int:question_id>/", views.vote, name = "vote")
]

"""
    Khi có request tới page với path: /polls/34/ (ví dụ) 
    -> Django load ecommerce và tìm đến urlpatterns ứng với polls/
    -> sau đó tách polls/ và gửi 34/ đến poll.urls 
"""
