from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가
import json

# Create your views here.
@require_http_methods(["GET"])
def get_post_detail(request, id):
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
def get_commentsInposts_detail(request, id):

	#post_id에 해당하는 전체 '댓글'을 조회
	if request.method == "GET":
		comment_all = Comment.objects.filter(post_id = id)

		#각 데이터를 Json형식으로 변환하여 list에 저장하기
		comment_json_all = []

		for comment in comment_all :
			comment_json = {
				"author" : comment.author_name,
				"content" : comment.content,
			}
			comment_json_all.append(comment_json)

		return JsonResponse({
			'status' : 200,
			'message' : '해당 게시글 전체 댓글 조회 성공',
			'data' : comment_json_all
		})
def get_postsIncategoriesOrdered_detail(request,id):

	#category_id에 해당하는 전체 'post'를 조회
	if request.method == "GET":
		postIncategory_all = CategoryLink.objects.filter(category_id = id).order_by('created')

		#각 데이터를 Json형식으로 변환하여 list에 저장하기
		postIncategory_json_all = []

		for postIncategory in postIncategory_all :
			postIncategory_json = {
				"postId" : postIncategory.post.id,
				"title" : postIncategory.post.title,
				"content" : postIncategory.post.content,
			}
			postIncategory_json_all.append(postIncategory_json)

		return JsonResponse({
			'status' : 200,
			'message' : '해당 카테고리 전체 게시글 조회 성공',
			'data' : postIncategory_json_all
		})

@require_http_methods(["GET","PATCH","DELETE"])
def post_detail(request, post_id):

    # post_id에 해당하는 단일 게시글 조회
    if request.method == "GET":
        post = get_object_or_404(Post, pk=post_id)

        post_json = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "status": post.status,
            "user": post.user.id,
        }
        
        return JsonResponse({
            'status': 200,
            'message': '게시글 단일 조회 성공',
            'data': post_json
        })
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_post = get_object_or_404(Post, pk=post_id)

        if 'title' in body:
            update_post.title = body['title']
        if 'content' in body:
            update_post.content = body['content']
        if 'status' in body:
            update_post.status = body['status']
    
        
        update_post.save()

        update_post_json = {
            "id": update_post.id,
            "title" : update_post.title,
            "content": update_post.content,
            "status": update_post.status,
            "user": update_post.user.id,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
        
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=post_id)
        delete_post.delete()

        return JsonResponse({
                'status': 200,
                'message': '게시글 삭제 성공',
                'data': None
        })


# 함수 데코레이터, 특정 http method만 허용
@require_http_methods(["POST","GET"])
def post_list(request):
    
    if request.method == "POST":
    
        # byte -> 문자열 -> python 딕셔너리
        body = json.loads(request.body.decode('utf-8'))
    
		    # 프론트에게서 user id를 넘겨받는다고 가정.
		    # 외래키 필드의 경우, 객체 자체를 전달해줘야하기 때문에
        # id를 기반으로 user 객체를 조회해서 가져옵니다 !
        user_id = body.get('user')
        user = get_object_or_404(User, pk=user_id)

	    # 새로운 데이터를 DB에 생성
        new_post = Post.objects.create(
            title = body['title'],
            content = body['content'],
            status = body['status'],
            user = user
        )
    
	    # Json 형태 반환 데이터 생성
        new_post_json = {
            "id": new_post.id,
            "title" : new_post.title,
            "content": new_post.content,
            "status": new_post.status,
            "user": new_post.user.id
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json
        })
    
    # 게시글 전체 조회
    if request.method == "GET":
        post_all = Post.objects.all()
    
		# 각 데이터를 Json 형식으로 변환하여 리스트에 저장
        post_json_all = []
        
        for post in post_all:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "content": post.content,
                "status": post.status,
                "user": post.user.id
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all
        })