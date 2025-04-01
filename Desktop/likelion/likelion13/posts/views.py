from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가

# Create your views here.
@require_http_methods(["GET"])
def get_post_detail(reqeust, id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "status" : post.status,
        "user" : post.user.username,
    }
    return JsonResponse({
        "status" : 200,
        "data": post_detail_json})
def get_comment_detail(request, id):
    comment = get_object_or_404(Comment, pk = id)
    comment_detail_json = {
        "author" : comment.author_name,
        "content" : comment.content,
    }
    return JsonResponse({
        "data": comment_detail_json})
