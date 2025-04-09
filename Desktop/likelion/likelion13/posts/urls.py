from django.urls import path
from posts.views import *

urlpatterns = [
    #Post관련
    #path('<int:id>', get_post_detail), # Post 내용 조회
    path('', post_list, name="post_list"), #Post 전체 조회
    path('<int:post_id>/', post_detail, name = 'post_detail'),#Post 단일 조회
    path('<int:id>/comments/', get_commentsInposts_detail), #해당 Post의 Comments_all 조회

    #Comment관련
    path('comment/<int:id>/',get_comment_detail),# Comment 내용 조회
    #Category 관련
    path('<int:id>/posts/', get_postsIncategoriesOrdered_detail), #해당 Category의 Posts_all 조회
]