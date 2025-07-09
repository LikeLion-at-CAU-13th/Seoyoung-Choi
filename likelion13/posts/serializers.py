### Model Serializer case

from rest_framework import serializers
from .models import Post,Comment
from .models import Image #12주차
from config.custom_api_exceptions import PostConflictException #14주차

class PostSerializer(serializers.ModelSerializer):

  class Meta:
		# 어떤 모델을 시리얼라이즈할 건지
    model = Post
		# 모델에서 어떤 필드를 가져올지
		# 전부 가져오고 싶을 때
    fields = "__all__"
    read_only_fields = ['id']
  # 중복된 게시글 제목이 있다면 예외 발생
  def validate(self, data):
    if Post.objects.filter(title=data['title']).exists():
      raise PostConflictException(detail=f"A post with title: '{data['title']}' already exists.")
    
    return data
  
    

class CommentSerializer(serializers.ModelSerializer):

  class Meta:
    model = Comment
    fields = "__all__"
  # 댓글 최소길이 조건
  def validate_content(self, value):
      if len(value.strip()) < 15:
          raise serializers.ValidationError("댓글은 최소 15자 이상 작성해야 합니다.")
      return value

# 12주차 - 이미지 API
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"