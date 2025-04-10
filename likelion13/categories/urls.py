from django.urls import path
from categories.views import *

urlpatterns = [
    #Category 관련
    path('posts/', get_posts_in_categories_ordered_detail), #해당 Category의 Posts_all 조회
]