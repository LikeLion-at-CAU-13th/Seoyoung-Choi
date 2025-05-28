from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가
import json

from .serializers import PostSerializer,CommentSerializer

# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

#로그아웃
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#permission 과제
from config.permissions import *

# Create your views here.
@require_http_methods(["GET"])
def get_post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
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
def get_comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)
    comment_detail_json = {
        "author" : comment.author_name,
        "content" : comment.content,
    }
    return JsonResponse({
        "data": comment_detail_json})
def get_comments_in_posts_detail(request):
    # 1. 쿼리 파라미터에서 post_id 받아오기
    post_id = request.GET.get("post_id")

    if not post_id:
        return JsonResponse({
            "status": 400,
            "message": "post_id 쿼리 파라미터가 필요합니다."
        }, status=400)

    # 2. 필터링 후 댓글 조회
    comment_all = Comment.objects.filter(post_id=post_id)

    # 3. JSON 변환
    comment_json_all = []
    for comment in comment_all:
        comment_json = {
            "author": comment.author_name,
            "content": comment.content,
        }
        comment_json_all.append(comment_json)

    return JsonResponse({
        'status': 200,
        'message': '해당 게시글 전체 댓글 조회 성공',
        'data': comment_json_all
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
    
class PostList(APIView):
    permission_classes = [TimePossible]
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = Post.objects.all()
		# 많은 post들을 받아오려면 (many=True) 써줘야 한다!
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostDetail(APIView):
    permission_classes = [TimePossible] # TimePossible에서 IsAuthen~~도 검사함.

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        #권한 검사
        if not WriterPossible().has_object_permission(request,self,post):
            return Response({"detail" : "수정 권한 없음"}, status = 403)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(): # update이니까 유효성 검사 필요
            serializer.save() #객체 생성 or 업데이트
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        #권한 검사
        if not WriterPossible().has_object_permission(request,self,post):
            return Response({"detail" : "삭제 권한 없음"}, status = 403)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentDetail(APIView):
    permission_classes = [TimePossible]
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk= comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def delete(self,request,comment_id):
        comment = get_object_or_404(Comment, id = comment_id)
        #권한 검사
        if not WriterPossible().has_object_permission(request,self,comment):
            return Response({"detail" : "삭제 권한 없음"}, status = 403)
        comment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    permission_classes = [TimePossible]
    def post(self,request,format=None):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        post_id = request.GET.get("post_id")
        if not post_id:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post_id = post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)