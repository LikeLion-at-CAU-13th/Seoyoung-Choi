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

# 12주차 이미지 API
from django.core.files.storage import default_storage  
from .serializers import ImageSerializer
from django.conf import settings
import boto3
# 12주차 Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# 12주차 중복 업로드
import uuid
import os
from rest_framework.parsers import MultiPartParser, FormParser

# 14주차
from config.custom_exceptions import *
from config.custom_api_exceptions import *
from datetime import datetime, timedelta

# Create your views here.
@require_http_methods(["GET"])
def get_post_detail(request, post_id):
    #post = get_object_or_404(Post, pk=post_id)
    #post_detail_json = {
        #"id" : post.id,
        #"title" : post.title,
        #"content" : post.content,
        #"status" : post.status,
        #"user" : post.user.username,
    #}
    #return JsonResponse({
        #"status" : 200,
        #"data": post_detail_json})
    try:
        post = Post.objects.get(id=post_id)
        post_detail_json = {
            "id" : post.id,
            "title" : post.title,
            "content" : post.content,
            "status" : post.status,
            "user" : post.user.username
        }
        return JsonResponse({
            "status" : 200,
            "data": post_detail_json})
    except Post.DoesNotExist:
        raise PostNotFoundException
    
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
    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="새로운 게시글을 생성합니다.",
        request_body=PostSerializer,
        responses={201: PostSerializer, 400: "잘못된 요청"}
    )
    def post(self, request, format=None):
        user_id = request.data.get("user")

        # user_id가 없거나 잘못된 경우 처리
        if not user_id:
            return Response({
                "success": False,
                "error": {
                    "code": "USER-ID-MISSING",
                    "message": "user 필드가 필요합니다.",
                    "status_code": 400
                }
            }, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "USER-NOT-FOUND",
                    "message": f"ID가 {user_id}인 사용자를 찾을 수 없습니다.",
                    "status_code": 404
                }
            }, status=404)

        # 하루 제한 검사
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if Post.objects.filter(user=user, created__gte=today_start).exists():
            raise DailyPostLimitException()

        # 직렬화 및 저장
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)  # ✅ 반드시 명시
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        operation_summary="게시글 목록 조회",
        operation_description="모든 게시글을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, format=None):
        posts = Post.objects.all()
		# 많은 post들을 받아오려면 (many=True) 써줘야 한다!
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostDetail(APIView):
    permission_classes = [TimePossible] # TimePossible에서 IsAuthen~~도 검사함.
    @swagger_auto_schema(
        operation_summary="게시글 단일 조회",
        operation_description="해당 id의 게시글을 조회합니다.",
        responses={200: PostSerializer, 404: "존재하지 않는 게시글"}
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    @swagger_auto_schema(
        operation_summary="게시글 단일 수정",
        operation_description="해당 id의 게시글을 수정합니다.",
        responses={200: PostSerializer,403: "권한 없음", 400: "잘못된 요청"}
    )
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
    @swagger_auto_schema(
        operation_summary="게시글 단일 삭제",
        operation_description="해당 id의 게시글을 삭제합니다.",
        responses={204: "삭제 완료", 403: "권한 없음", 404: "존재하지 않음"}
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        #권한 검사
        if not WriterPossible().has_object_permission(request,self,post):
            return Response({"detail" : "삭제 권한 없음"}, status = 403)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentDetail(APIView):
    permission_classes = [TimePossible]
    @swagger_auto_schema(
        operation_summary="댓글 단일 조회",
        operation_description="해당 id의 댓글을 조회합니다.",
        responses={200: CommentSerializer, 404: "존재하지 않는 댓글"}
    )
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk= comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    @swagger_auto_schema(
        operation_summary="댓글 단일 삭제",
        operation_description="해당 id의 댓글을 삭제합니다.",
        responses={204: "삭제 완료", 403: "권한 없음", 404: "존재하지 않음"}
    )
    def delete(self,request,comment_id):
        comment = get_object_or_404(Comment, id = comment_id)
        #권한 검사
        if not WriterPossible().has_object_permission(request,self,comment):
            return Response({"detail" : "삭제 권한 없음"}, status = 403)
        comment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    permission_classes = [TimePossible]
    @swagger_auto_schema(
        operation_summary="댓글 생성",
        operation_description="새로운 댓글을 생성합니다.",
        request_body=CommentSerializer,
        responses={201: CommentSerializer, 400: "잘못된 요청"}
    )
    def post(self,request,format=None):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="특정 게시글 댓글 조회",
        operation_description="해당 게시글의 댓글을 조회합니다.",
        responses={200: CommentSerializer(many=True)}
    )
    def get(self, request):
        post_id = request.GET.get("post_id")
        if not post_id:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post_id = post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
# 12주차 - 이미지 API
class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="이미지 업로드",
        operation_description="이미지를 S3에 업로드하고 URL을 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="업로드할 이미지 파일",
                required=True,
            )
        ],
        responses={201: ImageSerializer, 400: "이미지 없음", 500: "S3 업로드 실패"}
    )
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image file"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        # ✅ UUID 기반 고유 파일명 생성
        unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(image_file.name)[1]}"
        file_path = f"uploads/{unique_filename}"

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # S3에 파일 저장
        #file_path = f"uploads/{image_file.name}"
        # S3에 파일 업로드
        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path,
                Body=image_file.read(),
                ContentType=image_file.content_type,
            )
        except Exception as e:
            return Response({"error": f"S3 Upload Failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 업로드된 파일의 URL 생성
        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_path}"

        # DB에 저장
        image_instance = Image.objects.create(image_url=image_url)
        serializer = ImageSerializer(image_instance)


        return Response(serializer.data, status=status.HTTP_201_CREATED)