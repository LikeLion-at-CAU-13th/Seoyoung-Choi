from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가
import json

@require_http_methods(["GET"])
def get_posts_in_categories_ordered_detail(request):
    # 쿼리 파라미터 가져오기
    category_id = request.GET.get("category_id")

    if not category_id:
        return JsonResponse({
            "status": 400,
            "message": "category_id 쿼리 파라미터가 필요합니다."
        }, status=400)

    # 해당 카테고리의 게시글 조회
    post_in_category_all = CategoryLink.objects.filter(category_id=category_id).order_by('created')

    # JSON 응답 구성
    post_in_category_json_all = []
    for post_in_category in post_in_category_all:
        post_in_category_json = {
            "postId": post_in_category.post.id,
            "title": post_in_category.post.title,
            "content": post_in_category.post.content,
        }
        post_in_category_json_all.append(post_in_category_json)

    return JsonResponse({
        'status': 200,
        'message': '해당 카테고리 전체 게시글 조회 성공',
        'data': post_in_category_json_all
    })
