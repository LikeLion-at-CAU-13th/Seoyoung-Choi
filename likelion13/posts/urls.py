from django.urls import path
from posts.views import *

urlpatterns = [
    #Post관련
    #path('<int:id>', get_post_detail), # Post 내용 조회
    #path('', post_list, name="post_list"), #Post 전체 조회
    #path('<int:post_id>/', post_detail, name = 'post_detail'),#Post 단일 조회
    #path('comments/', get_comments_in_posts_detail), #해당 Post의 Comments_all 조회
    path('comments/', CommentList.as_view()),
    path('', PostList.as_view()), # post 전체 조회
    path('<int:post_id>/', PostDetail.as_view()), # post 개별 조회

    #Comment관련
    #path('comment/<int:comment_id>/',get_comment_detail),# Comment 단일 조회
    path('comment/<int:comment_id>/',CommentDetail.as_view()),
]